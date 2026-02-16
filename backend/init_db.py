import sys
import os
from pathlib import Path

# Add project root to path
current_file = Path(__file__).resolve()
backend_dir = current_file.parent
repo_root = backend_dir.parent
sys.path.insert(0, str(repo_root))

from backend.database import engine, Base
from backend.models import *

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

if __name__ == "__main__":
    init_db()
from sqlalchemy import text
from backend.database import engine
import logging

logger = logging.getLogger(__name__)

def migrate_db():
    """
    Perform database migrations.
    This is a simple MVP migration strategy.
    """
    try:
        with engine.connect() as conn:
            def safe_migrate(sql, success_msg):
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    if success_msg:
                        logger.info(success_msg)
                except Exception:
                    conn.rollback()

            # Check for upvotes column and add if missing
            # SQLite doesn't support IF NOT EXISTS in ALTER TABLE
            safe_migrate("ALTER TABLE issues ADD COLUMN upvotes INTEGER DEFAULT 0", "Migrated database: Added upvotes column.")

            # Check if index exists or create it
            safe_migrate("CREATE INDEX ix_issues_upvotes ON issues (upvotes)", "Migrated database: Added index on upvotes column.")

            # Add index on created_at for faster sorting
            safe_migrate("CREATE INDEX ix_issues_created_at ON issues (created_at)", "Migrated database: Added index on created_at column.")

            # Add index on status for faster filtering
            safe_migrate("CREATE INDEX ix_issues_status ON issues (status)", "Migrated database: Added index on status column.")

            # Add latitude column
            safe_migrate("ALTER TABLE issues ADD COLUMN latitude FLOAT", "Migrated database: Added latitude column.")

            # Add longitude column
            safe_migrate("ALTER TABLE issues ADD COLUMN longitude FLOAT", "Migrated database: Added longitude column.")

            # Add index on latitude for faster spatial queries
            safe_migrate("CREATE INDEX ix_issues_latitude ON issues (latitude)", "Migrated database: Added index on latitude column.")

            # Add index on longitude for faster spatial queries
            safe_migrate("CREATE INDEX ix_issues_longitude ON issues (longitude)", "Migrated database: Added index on longitude column.")

            # Add composite index for optimized spatial+status queries
            safe_migrate("CREATE INDEX ix_issues_status_lat_lon ON issues (status, latitude, longitude)", "Migrated database: Added composite index on status, latitude, longitude.")

            # Add location column
            safe_migrate("ALTER TABLE issues ADD COLUMN location VARCHAR", "Migrated database: Added location column.")

            # Add action_plan column
            safe_migrate("ALTER TABLE issues ADD COLUMN action_plan TEXT", "Migrated database: Added action_plan column.")

            # Add integrity_hash column for blockchain feature
            safe_migrate("ALTER TABLE issues ADD COLUMN integrity_hash VARCHAR", "Migrated database: Added integrity_hash column.")

            # Add previous_integrity_hash column for blockchain feature
            safe_migrate("ALTER TABLE issues ADD COLUMN previous_integrity_hash VARCHAR", "Migrated database: Added previous_integrity_hash column.")

            # Add parent_issue_id column for duplicate tracking
            safe_migrate("ALTER TABLE issues ADD COLUMN parent_issue_id INTEGER", "Migrated database: Added parent_issue_id column.")

            # Add index on parent_issue_id
            safe_migrate("CREATE INDEX ix_issues_parent_issue_id ON issues (parent_issue_id)", "Migrated database: Added index on parent_issue_id.")

            # Add index on user_email
            safe_migrate("CREATE INDEX ix_issues_user_email ON issues (user_email)", "Migrated database: Added index on user_email column.")

            # --- Grievance Migrations ---
            # Add latitude column to grievances
            safe_migrate("ALTER TABLE grievances ADD COLUMN latitude FLOAT", "Migrated database: Added latitude column to grievances.")

            # Add longitude column to grievances
            safe_migrate("ALTER TABLE grievances ADD COLUMN longitude FLOAT", "Migrated database: Added longitude column to grievances.")

            # Add address column to grievances
            safe_migrate("ALTER TABLE grievances ADD COLUMN address VARCHAR", "Migrated database: Added address column to grievances.")

            # Add index on latitude (grievances)
            safe_migrate("CREATE INDEX ix_grievances_latitude ON grievances (latitude)", None)

            # Add index on longitude (grievances)
            safe_migrate("CREATE INDEX ix_grievances_longitude ON grievances (longitude)", None)

            # Add composite index for spatial+status (grievances)
            safe_migrate("CREATE INDEX ix_grievances_status_lat_lon ON grievances (status, latitude, longitude)", "Migrated database: Added composite index on status, latitude, longitude for grievances.")

            # Add composite index for status+jurisdiction (grievances)
            safe_migrate("CREATE INDEX ix_grievances_status_jurisdiction ON grievances (status, current_jurisdiction_id)", "Migrated database: Added composite index on status, jurisdiction for grievances.")

            # Add issue_id column to grievances
            safe_migrate("ALTER TABLE grievances ADD COLUMN issue_id INTEGER", "Migrated database: Added issue_id column to grievances.")

            # Add index on issue_id (grievances)
            safe_migrate("CREATE INDEX ix_grievances_issue_id ON grievances (issue_id)", "Migrated database: Added index on issue_id for grievances.")

            # Add index on assigned_authority (grievances)
            safe_migrate("CREATE INDEX ix_grievances_assigned_authority ON grievances (assigned_authority)", "Migrated database: Added index on assigned_authority for grievances.")

            # Add composite index for category+status (grievances) - Optimized for filtering
            safe_migrate("CREATE INDEX ix_grievances_category_status ON grievances (category, status)", "Migrated database: Added composite index on category, status for grievances.")

            logger.info("Database migration check completed.")
    except Exception as e:
        logger.error(f"Database migration error: {e}")
