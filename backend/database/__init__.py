"""
Database package for Installment Fraud Detection System

This package contains all database-related components:
- Connection and session management
- Database models
- Utilities and migrations
- SQL initialization scripts
"""

# Import main database components for easy access
from .database import (
    DATABASE_URL, engine, SessionLocal, Base, get_db, create_tables
)

from .models import (
    # Models
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern,
    # Enums
    UserRole, RequestStatus, PlanStatus, PaymentStatus,
    AlertType, AlertSeverity, AlertStatus
)

from .database_utils import (
    init_database, check_database_connection, run_migrations,
    get_async_db, check_async_database_connection
)

# Export all for backward compatibility
__all__ = [
    # Database connection
    "DATABASE_URL", "engine", "SessionLocal", "Base", "get_db", "create_tables",
    
    # Models
    "User", "Business", "InstallmentRequest", "InstallmentPlan", "Payment",
    "FraudAlert", "FraudPattern",
    
    # Enums
    "UserRole", "RequestStatus", "PlanStatus", "PaymentStatus",
    "AlertType", "AlertSeverity", "AlertStatus",
    
    # Utilities
    "init_database", "check_database_connection", "run_migrations",
    "get_async_db", "check_async_database_connection"
]