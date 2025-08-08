"""
Database utilities for the Installment Fraud Detection System
"""
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import DATABASE_URL, Base, engine, get_db
import logging

logger = logging.getLogger(__name__)

# Async engine for async operations
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    """Dependency for async database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def init_database():
    """Initialize database with tables and sample data"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Check if we need to add sample data
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            
            if user_count == 0:
                logger.info("Adding sample data...")
                # Sample data will be added via init.sql
        
        # Initialize translations
        init_translations()
                
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def init_translations():
    """Initialize default translations"""
    try:
        # Import here to avoid circular imports
        from translation_models import Translation
        from translation_service import TranslationService
        
        # Get database session
        db = next(get_db())
        
        try:
            # Check if translations already exist
            existing_translations = db.query(Translation).first()
            
            if not existing_translations:
                logger.info("Seeding default translations...")
                translation_service = TranslationService(db)
                translation_service.seed_default_translations()
                logger.info("Default translations seeded successfully")
            else:
                logger.info("Translations already exist, skipping seed")
                
            return True
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Translation initialization failed: {e}")
        # Don't fail the entire startup for translation issues
        logger.warning("Continuing startup without translation seeding")
        return True  # Return True to not block startup

def check_database_connection():
    """Check if database connection is working"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

async def check_async_database_connection():
    """Check if async database connection is working"""
    try:
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Async database connection successful")
        return True
    except Exception as e:
        logger.error(f"Async database connection failed: {e}")
        return False

def run_migrations():
    """Run database migrations"""
    try:
        from alembic.config import Config
        from alembic import command
        
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False

if __name__ == "__main__":
    # Test database connections
    print("Testing database connections...")
    
    # Test sync connection
    if check_database_connection():
        print("✅ Sync database connection working")
    else:
        print("❌ Sync database connection failed")
    
    # Test async connection
    async def test_async():
        if await check_async_database_connection():
            print("✅ Async database connection working")
        else:
            print("❌ Async database connection failed")
    
    asyncio.run(test_async())
    
    # Initialize database
    if init_database():
        print("✅ Database initialized successfully")
    else:
        print("❌ Database initialization failed")