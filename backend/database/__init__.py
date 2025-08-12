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
from .connection import Base, engine, SessionLocal, get_db, create_tables, DATABASE_URL
from .models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment, 
    FraudAlert, FraudPattern,
    UserRole, RequestStatus, PlanStatus, PaymentStatus, 
    AlertType, AlertSeverity, AlertStatus
)
from .utils import (
    init_database, check_database_connection, run_migrations,
    get_async_db, check_async_database_connection
)

__all__ = [
    # Connection
    "Base", "engine", "SessionLocal", "get_db", "create_tables", "DATABASE_URL",
    
    # Models
    "User", "Business", "InstallmentRequest", "InstallmentPlan", "Payment",
    "FraudAlert", "FraudPattern",
    
    # Enums
    "UserRole", "RequestStatus", "PlanStatus", "PaymentStatus",
    "AlertType", "AlertSeverity", "AlertStatus",
    
    # Utils
    "init_database", "check_database_connection", "run_migrations",
    "get_async_db", "check_async_database_connection"
]