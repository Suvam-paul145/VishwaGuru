import json
import logging
from database import SessionLocal
from models import Issue
from ai_interfaces import get_ai_services
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

async def generate_and_save_action_plan(issue_id: int, description: str, category: str, image_path: str = None):
    """
    Background task to generate action plan using AI and update the database.
    """
    logger.info(f"Starting background action plan generation for issue {issue_id}")

    db = SessionLocal()
    try:
        # Generate Action Plan (AI)
        ai_services = get_ai_services()

        # This is already async, so we await it directly
        action_plan_data = await ai_services.action_plan_service.generate_action_plan(description, category, image_path)

        # Serialize action plan to JSON string for storage
        action_plan_json = json.dumps(action_plan_data) if action_plan_data else None

        # Fetch the issue again to ensure we have the latest state (though it should be unchanged mostly)
        issue = db.query(Issue).filter(Issue.id == issue_id).first()
        if issue:
            issue.action_plan = action_plan_json
            db.commit()
            logger.info(f"Action plan saved for issue {issue_id}")
        else:
            logger.error(f"Issue {issue_id} not found during background task")

    except Exception as e:
        logger.error(f"Error in background action plan generation for issue {issue_id}: {e}", exc_info=True)
        # Optionally update DB with error status if we had one
    finally:
        db.close()
