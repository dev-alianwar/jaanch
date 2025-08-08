"""
Startup script for the Installment Fraud Detection System
Handles database migrations and initial data seeding
"""
import logging
import sys
from database_utils import check_database_connection, run_migrations, init_database

logger = logging.getLogger(__name__)

def startup_sequence():
    """Run the complete startup sequence"""
    logger.info("Starting application startup sequence...")
    
    try:
        # Step 1: Check database connection
        logger.info("Step 1: Checking database connection...")
        if not check_database_connection():
            logger.error("Database connection failed!")
            return False
        
        # Step 2: Run migrations
        logger.info("Step 2: Running database migrations...")
        try:
            if not run_migrations():
                logger.warning("Database migrations had issues, continuing...")
        except Exception as e:
            logger.warning(f"Migration error (continuing): {e}")
        
        # Step 3: Initialize database (includes translation seeding)
        logger.info("Step 3: Initializing database and seeding data...")
        if not init_database():
            logger.warning("Database initialization had issues")
            return False
        
        logger.info("Startup sequence completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Startup sequence failed with error: {e}")
        return False

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    success = startup_sequence()
    sys.exit(0 if success else 1)