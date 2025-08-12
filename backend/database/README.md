# Database Package

This directory contains all database-related components for the Installment Fraud Detection System.

## Directory Structure

```
database/
├── __init__.py              # Package exports and backward compatibility
├── README.md               # This file
├── database.py             # Database connection and session management
├── database_utils.py       # Database utilities and initialization
├── models.py               # SQLAlchemy models and enums
├── init.sql                # Database initialization SQL script
├── alembic.ini             # Alembic configuration for migrations
└── migrations/             # Database migrations (Alembic)
    ├── alembic/
    ├── env.py
    ├── script.py.mako
    └── versions/
```

## Components

### Core Database (`database.py`)
- Database connection setup
- Session management
- Base model class
- Database dependency for FastAPI

### Models (`models.py`)
- All SQLAlchemy models:
  - `User` - User accounts (customers, businesses, admins)
  - `Business` - Business information
  - `InstallmentRequest` - Installment purchase requests
  - `InstallmentPlan` - Approved installment plans
  - `Payment` - Individual payments
  - `FraudAlert` - Fraud detection alerts
  - `FraudPattern` - Detected fraud patterns

- Enums for status tracking:
  - `UserRole`, `RequestStatus`, `PlanStatus`, `PaymentStatus`
  - `AlertType`, `AlertSeverity`, `AlertStatus`

### Utilities (`database_utils.py`)
- Database initialization
- Connection health checks
- Migration management
- Async database support
- Translation system initialization

### Initialization (`init.sql`)
- Database schema creation
- Indexes and constraints
- Sample data for development
- Triggers and functions

### Migrations (`migrations/`)
- Alembic migration files
- Version control for database schema
- Upgrade/downgrade scripts

## Usage

### Basic Import
```python
from database import User, get_db, engine
```

### Session Management
```python
from database import get_db

def my_function(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
```

### Model Usage
```python
from database import User, UserRole

# Create user
user = User(
    email="test@example.com",
    password_hash="hashed_password",
    role=UserRole.CUSTOMER,
    first_name="Test",
    last_name="User"
)
```

### Database Initialization
```python
from database import init_database, check_database_connection

# Check connection
if check_database_connection():
    print("Database connected")

# Initialize database
if init_database():
    print("Database initialized")
```

## Migration Commands

### Create Migration
```bash
cd database
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
cd database
alembic upgrade head
```

### Check Migration Status
```bash
cd database
alembic current
alembic history
```

## Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

## Backward Compatibility

The package maintains backward compatibility with existing imports:
- Old: `from models import User`
- New: `from database import User`
- Both work during transition period

## Database Schema

### Users Table
- Stores all user accounts (customers, businesses, admins)
- Role-based access control
- Email-based authentication

### Business Table
- Business information and verification status
- Linked to user accounts

### Installment System
- `installment_requests` - Purchase requests
- `installment_plans` - Approved payment plans
- `payments` - Individual payment records

### Fraud Detection
- `fraud_alerts` - Detected suspicious activities
- `fraud_patterns` - Pattern analysis results

## Performance Considerations

- Indexes on frequently queried columns
- Connection pooling configured
- Async support for high-throughput operations
- Proper foreign key constraints

## Security

- Password hashing with bcrypt
- SQL injection protection via SQLAlchemy
- Role-based access control
- Audit trails with timestamps

This organized structure makes database management more maintainable and scalable.