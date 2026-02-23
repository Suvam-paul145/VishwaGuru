"""
Public Resolution Scorecard Router (Issue #286)

Provides a cached, public endpoint for department/region performance rankings.
"""

import time
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.scorecard_service import ScorecardService

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple TTL-based cache
_scorecard_cache: dict = {}
_cache_timestamp: float = 0.0
CACHE_TTL_SECONDS = 300  # 5 minutes


def _get_cached_scorecard(db: Session) -> dict:
    """Return cached scorecard data, refreshing if stale."""
    global _scorecard_cache, _cache_timestamp

    now = time.time()
    if _scorecard_cache and (now - _cache_timestamp) < CACHE_TTL_SECONDS:
        return _scorecard_cache

    logger.info("Refreshing scorecard cache...")
    _scorecard_cache = ScorecardService.get_full_scorecard(db)
    _cache_timestamp = now
    return _scorecard_cache


@router.get("/api/scorecard", tags=["Scorecard"])
def get_scorecard(db: Session = Depends(get_db)):
    """
    Public Resolution Scorecard — ranks departments and regions
    by grievance resolution performance metrics.

    This endpoint is public (no auth required) and cached for high-traffic access.
    """
    return _get_cached_scorecard(db)
