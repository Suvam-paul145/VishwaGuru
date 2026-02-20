import sys
import os
import logging

# Add project root to sys.path to ensure 'backend' module is importable
# This allows running the script directly from anywhere
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, project_root)

from backend.database import SessionLocal
from backend.civic_intelligence import civic_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Daily Refinement Job...")
    try:
        db = SessionLocal()
        logger.info("Database session established.")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return

    try:
        result = civic_engine.refine_daily(db)
        logger.info("Daily Refinement Job completed successfully.")

        # Sanitize summary for logging to avoid sensitive location data
        safe_summary = {
            "score": result.get("score"),
            "top_concern": result.get("top_concern"),
            "metrics": result.get("metrics")
        }
        logger.info(f"Summary: {safe_summary}")
    except Exception as e:
        logger.error(f"Daily Refinement Job failed: {e}", exc_info=True)
    finally:
        db.close()

if __name__ == "__main__":
    main()
