# Backward compatibility - imports from database package
from database.connection import (
    Base, engine, SessionLocal, get_db, create_tables, DATABASE_URL
)

# Re-export for backward compatibility
__all__ = ["Base", "engine", "SessionLocal", "get_db", "create_tables", "DATABASE_URL"]