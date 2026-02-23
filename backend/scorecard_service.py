"""
Public Resolution Scorecard Service (Issue #286)

Aggregates grievance resolution metrics by department and region,
applies normalization to prevent gaming, and generates trend data.
"""

import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract

from backend.models import Grievance, GrievanceStatus

logger = logging.getLogger(__name__)

# Weights for normalized composite score
WEIGHT_RESOLUTION_RATE = 0.50
WEIGHT_AVG_TIME_PENALTY = 0.30
WEIGHT_REOPEN_PENALTY = 0.20

# Baseline SLA hours used for time penalty normalization
BASELINE_SLA_HOURS = 72.0

# Minimum grievances required for a valid scorecard entry (anti-gaming)
MIN_GRIEVANCES_THRESHOLD = 3


class ScorecardService:
    """Service for computing department/region resolution scorecards."""

    @staticmethod
    def _compute_score(resolution_rate: float, avg_hours: float, reopen_rate: float) -> float:
        """
        Compute a normalized composite score (0–100).

        Formula:
          score = W_res × resolution_rate
                - W_time × min(avg_hours / BASELINE, 1.0) × 100
                - W_reopen × reopen_rate

        Higher is better. Clamped to [0, 100].
        """
        time_penalty = min(avg_hours / BASELINE_SLA_HOURS, 1.0) * 100.0
        raw = (
            WEIGHT_RESOLUTION_RATE * resolution_rate
            - WEIGHT_AVG_TIME_PENALTY * time_penalty
            - WEIGHT_REOPEN_PENALTY * reopen_rate
        )
        return round(max(0.0, min(100.0, raw)), 2)

    @staticmethod
    def _aggregate_by(db: Session, group_column) -> List[dict]:
        """
        Aggregate grievance metrics grouped by the given column.

        Returns a list of dicts sorted by composite score descending.
        """
        now = datetime.now(timezone.utc)

        # Base aggregation query
        rows = (
            db.query(
                group_column.label("name"),
                func.count(Grievance.id).label("total"),
                func.sum(
                    case(
                        (Grievance.status == GrievanceStatus.RESOLVED, 1),
                        else_=0
                    )
                ).label("resolved"),
                func.sum(
                    case(
                        (Grievance.status == GrievanceStatus.OPEN, 1),
                        else_=0
                    )
                ).label("open_count"),
                func.sum(
                    case(
                        (Grievance.status == GrievanceStatus.ESCALATED, 1),
                        else_=0
                    )
                ).label("escalated"),
                func.avg(
                    case(
                        (
                            Grievance.resolved_at.isnot(None),
                            func.julianday(Grievance.resolved_at) - func.julianday(Grievance.created_at)
                        ),
                        else_=None
                    )
                ).label("avg_days"),
            )
            .filter(group_column.isnot(None))
            .filter(group_column != "")
            .group_by(group_column)
            .all()
        )

        entries = []
        for row in rows:
            total = row.total or 0
            if total < MIN_GRIEVANCES_THRESHOLD:
                continue

            resolved = row.resolved or 0
            escalated = row.escalated or 0
            open_count = row.open_count or 0
            avg_days = row.avg_days or 0.0

            resolution_rate = (resolved / total) * 100.0 if total > 0 else 0.0
            avg_hours = avg_days * 24.0
            reopen_rate = (escalated / total) * 100.0 if total > 0 else 0.0
            score = ScorecardService._compute_score(resolution_rate, avg_hours, reopen_rate)

            entries.append({
                "name": row.name,
                "total_grievances": total,
                "resolved_count": resolved,
                "open_count": open_count,
                "escalated_count": escalated,
                "resolution_rate": round(resolution_rate, 2),
                "avg_resolution_hours": round(avg_hours, 2),
                "reopen_rate": round(reopen_rate, 2),
                "score": score,
            })

        # Sort by score descending
        entries.sort(key=lambda e: e["score"], reverse=True)

        # Assign ranks
        for i, entry in enumerate(entries, start=1):
            entry["rank"] = i

        return entries

    @staticmethod
    def get_department_scorecard(db: Session) -> List[dict]:
        """Get scorecard entries grouped by department (category)."""
        return ScorecardService._aggregate_by(db, Grievance.category)

    @staticmethod
    def get_region_scorecard(db: Session) -> List[dict]:
        """Get scorecard entries grouped by region (district)."""
        return ScorecardService._aggregate_by(db, Grievance.district)

    @staticmethod
    def _get_trend_data(db: Session, group_column, periods: int = 6) -> Dict[str, List[dict]]:
        """
        Get monthly resolution-rate trend data for each group over the last N months.
        """
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=periods * 30)

        rows = (
            db.query(
                group_column.label("name"),
                func.strftime("%Y-%m", Grievance.created_at).label("period"),
                func.count(Grievance.id).label("total"),
                func.sum(
                    case(
                        (Grievance.status == GrievanceStatus.RESOLVED, 1),
                        else_=0
                    )
                ).label("resolved"),
            )
            .filter(group_column.isnot(None))
            .filter(group_column != "")
            .filter(Grievance.created_at >= cutoff)
            .group_by(group_column, func.strftime("%Y-%m", Grievance.created_at))
            .all()
        )

        trends: Dict[str, List[dict]] = {}
        for row in rows:
            total = row.total or 0
            resolved = row.resolved or 0
            rate = (resolved / total) * 100.0 if total > 0 else 0.0
            name = row.name

            if name not in trends:
                trends[name] = []
            trends[name].append({
                "period": row.period,
                "resolution_rate": round(rate, 2),
            })

        # Sort each group's trends chronologically
        for name in trends:
            trends[name].sort(key=lambda t: t["period"])

        return trends

    @staticmethod
    def get_full_scorecard(db: Session) -> dict:
        """
        Get the complete scorecard response with departments, regions, and trends.
        """
        try:
            departments = ScorecardService.get_department_scorecard(db)
            regions = ScorecardService.get_region_scorecard(db)
            dept_trends = ScorecardService._get_trend_data(db, Grievance.category)
            region_trends = ScorecardService._get_trend_data(db, Grievance.district)

            return {
                "departments": departments,
                "regions": regions,
                "department_trends": dept_trends,
                "region_trends": region_trends,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "cache_ttl_seconds": 300,
            }
        except Exception as e:
            logger.error(f"Error generating scorecard: {e}", exc_info=True)
            return {
                "departments": [],
                "regions": [],
                "department_trends": {},
                "region_trends": {},
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "cache_ttl_seconds": 300,
            }
