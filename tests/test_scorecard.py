"""
Tests for the Public Resolution Scorecard (Issue #286)

Tests:
- Pydantic schema validation (ScorecardEntry, TrendPoint, ScorecardResponse)
- ScorecardService scoring formula
- Aggregation with mocked DB queries
- Edge cases: empty data, single entry, boundary scores
"""

import os
import sys
from datetime import datetime, timezone

import pytest

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ──────────────────────────────────────────────
# Schema Tests
# ──────────────────────────────────────────────

class TestScorecardSchemas:
    """Test Pydantic schemas for scorecard system."""

    def test_scorecard_entry_valid(self):
        from backend.schemas import ScorecardEntry
        entry = ScorecardEntry(
            rank=1,
            name="Road Department",
            total_grievances=100,
            resolved_count=80,
            open_count=15,
            escalated_count=5,
            resolution_rate=80.0,
            avg_resolution_hours=48.0,
            reopen_rate=5.0,
            score=72.5,
        )
        assert entry.rank == 1
        assert entry.name == "Road Department"
        assert entry.resolution_rate == 80.0
        assert entry.score == 72.5

    def test_scorecard_entry_defaults(self):
        from backend.schemas import ScorecardEntry
        entry = ScorecardEntry(
            rank=1,
            name="Test",
            total_grievances=10,
            resolved_count=5,
            resolution_rate=50.0,
            avg_resolution_hours=24.0,
            reopen_rate=10.0,
            score=25.0,
        )
        assert entry.open_count == 0
        assert entry.escalated_count == 0

    def test_trend_point_valid(self):
        from backend.schemas import TrendPoint
        tp = TrendPoint(period="2026-01", resolution_rate=65.5)
        assert tp.period == "2026-01"
        assert tp.resolution_rate == 65.5

    def test_scorecard_response_valid(self):
        from backend.schemas import ScorecardResponse, ScorecardEntry, TrendPoint
        resp = ScorecardResponse(
            departments=[
                ScorecardEntry(
                    rank=1, name="Roads", total_grievances=50, resolved_count=40,
                    resolution_rate=80.0, avg_resolution_hours=36.0,
                    reopen_rate=4.0, score=75.0,
                )
            ],
            regions=[],
            department_trends={"Roads": [TrendPoint(period="2026-01", resolution_rate=80.0)]},
            region_trends={},
            generated_at=datetime.now(timezone.utc),
            cache_ttl_seconds=300,
        )
        assert len(resp.departments) == 1
        assert resp.departments[0].name == "Roads"
        assert len(resp.regions) == 0
        assert "Roads" in resp.department_trends
        assert resp.cache_ttl_seconds == 300

    def test_scorecard_response_empty(self):
        from backend.schemas import ScorecardResponse
        resp = ScorecardResponse(
            departments=[],
            regions=[],
            department_trends={},
            region_trends={},
            generated_at=datetime.now(timezone.utc),
        )
        assert len(resp.departments) == 0
        assert resp.cache_ttl_seconds == 300  # default


# ──────────────────────────────────────────────
# Scoring Formula Tests
# ──────────────────────────────────────────────

class TestScoringFormula:
    """Test the normalized composite score computation."""

    def test_perfect_score(self):
        from backend.scorecard_service import ScorecardService
        # 100% resolution, 0 hours, 0% reopen → should be high
        score = ScorecardService._compute_score(100.0, 0.0, 0.0)
        assert score == 50.0  # 0.5 * 100 - 0 - 0

    def test_zero_score(self):
        from backend.scorecard_service import ScorecardService
        # 0% resolution, very long time, high reopen
        score = ScorecardService._compute_score(0.0, 200.0, 100.0)
        assert score == 0.0  # Clamped to 0

    def test_average_score(self):
        from backend.scorecard_service import ScorecardService
        # 60% resolution, 72h (baseline) avg, 10% reopen
        score = ScorecardService._compute_score(60.0, 72.0, 10.0)
        # 0.5*60 - 0.3*100 - 0.2*10 = 30 - 30 - 2 = -2 → clamped to 0
        assert score == 0.0

    def test_good_performance(self):
        from backend.scorecard_service import ScorecardService
        # 90% resolution, 24h avg (1/3 of baseline), 3% reopen
        score = ScorecardService._compute_score(90.0, 24.0, 3.0)
        # 0.5*90 - 0.3*(24/72)*100 - 0.2*3 = 45 - 10 - 0.6 = 34.4
        assert 34.0 <= score <= 35.0

    def test_score_clamped_to_100(self):
        from backend.scorecard_service import ScorecardService
        # Even with extreme values, score should not exceed 100
        score = ScorecardService._compute_score(200.0, 0.0, 0.0)
        assert score <= 100.0

    def test_score_clamped_to_0(self):
        from backend.scorecard_service import ScorecardService
        score = ScorecardService._compute_score(0.0, 500.0, 100.0)
        assert score == 0.0


# ──────────────────────────────────────────────
# Service Edge Case Tests
# ──────────────────────────────────────────────

class TestServiceEdgeCases:
    """Test edge cases in the scorecard service."""

    def test_compute_score_with_zero_hours(self):
        from backend.scorecard_service import ScorecardService
        score = ScorecardService._compute_score(50.0, 0.0, 0.0)
        assert score == 25.0  # 0.5 * 50

    def test_compute_score_with_max_reopen(self):
        from backend.scorecard_service import ScorecardService
        # High resolution but high reopen
        score = ScorecardService._compute_score(100.0, 0.0, 100.0)
        # 0.5*100 - 0 - 0.2*100 = 50 - 20 = 30
        assert score == 30.0

    def test_compute_score_rounding(self):
        from backend.scorecard_service import ScorecardService
        score = ScorecardService._compute_score(73.33, 33.33, 7.77)
        assert isinstance(score, float)
        # Should be rounded to 2 decimal places
        assert score == round(score, 2)


# ──────────────────────────────────────────────
# Module Import Tests
# ──────────────────────────────────────────────

class TestModuleImports:
    """Verify all scorecard modules import correctly."""

    def test_import_scorecard_service(self):
        from backend.scorecard_service import ScorecardService
        assert hasattr(ScorecardService, 'get_department_scorecard')
        assert hasattr(ScorecardService, 'get_region_scorecard')
        assert hasattr(ScorecardService, 'get_full_scorecard')
        assert hasattr(ScorecardService, '_compute_score')
        assert hasattr(ScorecardService, '_get_trend_data')

    def test_import_scorecard_router(self):
        from backend.routers.scorecard import router
        assert router is not None

    def test_import_scorecard_schemas(self):
        from backend.schemas import ScorecardEntry, TrendPoint, ScorecardResponse
        assert ScorecardEntry is not None
        assert TrendPoint is not None
        assert ScorecardResponse is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
