# Complete Database Guide

## Overview

This guide covers all database-related components for the Installment Fraud Detection System, including setup, models, utilities, and maintenance.

## Directory Structure

```
database/
├── __init__.py              # Package exports and backward compatibility
├── COMPLETE_DATABASE_GUIDE.md # This comprehensive guide
├── database.py             # Database connection and session management
├── database_utils.py       # Database utilities and initialization
├── models.py               # SQLAlchemy models and enums
├── init.sql                # Database initialization SQL script
├── alembic.ini             # Alembic configuration for migrations
└── migrations/             # Database migrations (Alembic)
    ├── env.py
    ├── script.py.mako
    └── versions/
```

## Database Models

### Core Models

#### User Model
Stores all user accounts with role-based access control.

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)
```

**Relationships:**
- One-to-many with Business (for business owners)
- One-to-many with InstallmentRequest (as customer)
- One-to-many with InstallmentPlan (as customer)
- One-to-many with FraudAlert
- One-to-many with FraudPattern

#### Business Model
Stores business information and verification status.

```python
class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    business_name = Column(String(255), nullable=False)
    business_type = Column(String(100))
    address = Column(Text)
    phone = Column(String(20))
    registration_number = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=False, index=True)
```

#### InstallmentRequest Model
Stores customer requests for installment purchases.

```python
class InstallmentRequest(Base):
    __tablename__ = "installment_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text)
    product_value = Column(Numeric(12, 2), nullable=False)
    installment_months = Column(Integer, nullable=False)
    monthly_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING, index=True)
    business_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

#### InstallmentPlan Model
Stores approved installment payment plans.

```python
class InstallmentPlan(Base):
    __tablename__ = "installment_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("installment_requests.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    total_amount = Column(Numeric(12, 2), nullable=False)
    paid_amount = Column(Numeric(12, 2), default=0)
    remaining_amount = Column(Numeric(12, 2), nullable=False)
    total_installments = Column(Integer, nullable=False)
    paid_installments = Column(Integer, default=0)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    status = Column(SQLEnum(PlanStatus), default=PlanStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### Payment Model
Stores individual payment records for installment plans.

```python
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("installment_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    paid_date = Column(Date)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

#### FraudAlert Model
Stores fraud detection alerts and investigations.

```python
class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    description = Column(Text, nullable=False)
    alert_metadata = Column(JSONB)
    severity = Column(SQLEnum(AlertSeverity), nullable=False)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved_at = Column(DateTime(timezone=True))
```

#### FraudPattern Model
Stores detected fraud patterns and risk analysis.

```python
class FraudPattern(Base):
    __tablename__ = "fraud_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    pattern_type = Column(String(100), nullable=False, index=True)
    pattern_data = Column(JSONB, nullable=False)
    risk_score = Column(Numeric(3, 2), nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
```

### Enums

#### UserRole
```python
class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    BUSINESS = "business"
    CUSTOMER = "customer"
```

#### RequestStatus
```python
class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

#### PlanStatus
```python
class PlanStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"
```

#### PaymentStatus
```python
class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
```

#### AlertType
```python
class AlertType(str, enum.Enum):
    RAPID_REQUESTS = "rapid_requests"
    HIGH_DEBT_RATIO = "high_debt_ratio"
    CROSS_BUSINESS_CHAIN = "cross_business_chain"
    PAYMENT_DEFAULT_PATTERN = "payment_default_pattern"
```

#### AlertSeverity
```python
class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

#### AlertStatus
```python
class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"
```

## Database Connection and Session Management

### Connection Setup
```python
from database import engine, SessionLocal, get_db

# Direct connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))

# Session usage
db = SessionLocal()
try:
    users = db.query(User).all()
finally:
    db.close()

# FastAPI dependency
def my_endpoint(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### Async Support
```python
from database.database_utils import get_async_db, async_engine

async def async_operation():
    async with get_async_db() as db:
        result = await db.execute(select(User))
        return result.scalars().all()
```

## Database Utilities

### Initialization
```python
from database.database_utils import init_database, check_database_connection

# Check connection
if check_database_connection():
    print("Database connected successfully")

# Initialize database with tables and sample data
if init_database():
    print("Database initialized successfully")
```

### Migration Management
```python
from database.database_utils import run_migrations

# Run all pending migrations
if run_migrations():
    print("Migrations completed successfully")
```

### Translation System
```python
from database.database_utils import init_translations

# Initialize default translations
if init_translations():
    print("Translations initialized successfully")
```

## Database Operations

### Basic CRUD Operations

#### Create User
```python
from database import User, UserRole, SessionLocal

db = SessionLocal()
try:
    user = User(
        email="user@example.com",
        password_hash="hashed_password",
        role=UserRole.CUSTOMER,
        first_name="John",
        last_name="Doe",
        phone="+1234567890"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user: {user.id}")
finally:
    db.close()
```

#### Query Users
```python
# Get all users
users = db.query(User).all()

# Filter by role
customers = db.query(User).filter(User.role == UserRole.CUSTOMER).all()

# Get user by email
user = db.query(User).filter(User.email == "user@example.com").first()

# Get user with relationships
user_with_businesses = db.query(User).options(joinedload(User.businesses)).first()
```

#### Update User
```python
user = db.query(User).filter(User.email == "user@example.com").first()
if user:
    user.first_name = "Jane"
    user.updated_at = func.now()
    db.commit()
```

#### Delete User
```python
user = db.query(User).filter(User.email == "user@example.com").first()
if user:
    db.delete(user)
    db.commit()
```

### Complex Queries

#### Customer Installment History
```python
from sqlalchemy.orm import joinedload

def get_customer_history(customer_id: str, db: Session):
    return db.query(InstallmentPlan)\
        .options(
            joinedload(InstallmentPlan.business),
            joinedload(InstallmentPlan.request),
            joinedload(InstallmentPlan.payments)
        )\
        .filter(InstallmentPlan.customer_id == customer_id)\
        .order_by(InstallmentPlan.created_at.desc())\
        .all()
```

#### Fraud Pattern Analysis
```python
def get_high_risk_customers(db: Session, risk_threshold: float = 0.7):
    return db.query(User)\
        .join(FraudPattern)\
        .filter(FraudPattern.risk_score >= risk_threshold)\
        .distinct()\
        .all()
```

#### Business Analytics
```python
def get_business_stats(business_id: str, db: Session):
    total_requests = db.query(InstallmentRequest)\
        .filter(InstallmentRequest.business_id == business_id)\
        .count()
    
    approved_requests = db.query(InstallmentRequest)\
        .filter(
            InstallmentRequest.business_id == business_id,
            InstallmentRequest.status == RequestStatus.APPROVED
        ).count()
    
    total_amount = db.query(func.sum(InstallmentPlan.total_amount))\
        .filter(InstallmentPlan.business_id == business_id)\
        .scalar() or 0
    
    return {
        "total_requests": total_requests,
        "approved_requests": approved_requests,
        "approval_rate": approved_requests / total_requests if total_requests > 0 else 0,
        "total_amount": float(total_amount)
    }
```

## Migration Management

### Alembic Configuration
The database uses Alembic for migration management. Configuration is in `alembic.ini`.

### Common Migration Commands
```bash
# Navigate to database directory
cd database

# Check current migration status
alembic current

# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Add new column to users table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### Migration Best Practices
1. **Always review auto-generated migrations** before applying
2. **Test migrations on development data** first
3. **Backup production database** before major migrations
4. **Use descriptive migration messages**
5. **Handle data migrations separately** if needed

## Performance Optimization

### Indexes
The database includes strategic indexes for performance:

```sql
-- User indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Installment request indexes
CREATE INDEX idx_installment_requests_customer ON installment_requests(customer_id);
CREATE INDEX idx_installment_requests_business ON installment_requests(business_id);
CREATE INDEX idx_installment_requests_status ON installment_requests(status);
CREATE INDEX idx_installment_requests_created ON installment_requests(created_at);

-- Installment plan indexes
CREATE INDEX idx_installment_plans_customer ON installment_plans(customer_id);
CREATE INDEX idx_installment_plans_business ON installment_plans(business_id);
CREATE INDEX idx_installment_plans_status ON installment_plans(status);
CREATE INDEX idx_installment_plans_dates ON installment_plans(start_date, end_date);

-- Payment indexes
CREATE INDEX idx_payments_plan ON payments(plan_id);
CREATE INDEX idx_payments_due_date ON payments(due_date);
CREATE INDEX idx_payments_status ON payments(status);

-- Fraud detection indexes
CREATE INDEX idx_fraud_alerts_customer ON fraud_alerts(customer_id);
CREATE INDEX idx_fraud_alerts_type ON fraud_alerts(alert_type);
CREATE INDEX idx_fraud_alerts_created ON fraud_alerts(created_at);
CREATE INDEX idx_fraud_patterns_customer ON fraud_patterns(customer_id);
CREATE INDEX idx_fraud_patterns_risk ON fraud_patterns(risk_score);
```

### Connection Pooling
```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Number of connections to maintain
    max_overflow=30,       # Additional connections when needed
    pool_pre_ping=True,    # Validate connections before use
    pool_recycle=3600      # Recycle connections every hour
)
```

### Query Optimization Tips
1. **Use eager loading** for relationships you'll access
2. **Limit result sets** with `.limit()` and pagination
3. **Use specific columns** instead of `SELECT *`
4. **Batch operations** for multiple inserts/updates
5. **Use database functions** for aggregations

## Security Considerations

### Data Protection
- **Password hashing**: All passwords are hashed using bcrypt
- **UUID primary keys**: Prevent enumeration attacks
- **SQL injection protection**: SQLAlchemy ORM provides protection
- **Sensitive data encryption**: Consider encrypting PII fields

### Access Control
- **Role-based permissions**: Implemented at application level
- **Database user permissions**: Use least-privilege principle
- **Connection encryption**: Use SSL/TLS for database connections
- **Audit logging**: Track all data access and modifications

### Backup and Recovery
```bash
# Create backup
pg_dump -h localhost -U username -d database_name > backup.sql

# Restore backup
psql -h localhost -U username -d database_name < backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U username -d database_name > "backup_${DATE}.sql"
```

## Troubleshooting

### Common Issues

#### Connection Problems
```python
# Test connection
from database.database_utils import check_database_connection
if not check_database_connection():
    print("Database connection failed")
    # Check DATABASE_URL environment variable
    # Verify PostgreSQL is running
    # Check firewall settings
```

#### Migration Issues
```bash
# Check migration status
alembic current

# If migrations are out of sync
alembic stamp head  # Mark current state as up-to-date

# If migration fails
alembic downgrade -1  # Rollback and fix issue
```

#### Performance Issues
```python
# Enable SQL logging for debugging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Use EXPLAIN to analyze queries
result = db.execute(text("EXPLAIN ANALYZE SELECT * FROM users WHERE role = 'customer'"))
print(result.fetchall())
```

### Monitoring
```python
# Connection pool status
from database import engine
pool = engine.pool
print(f"Pool size: {pool.size()}")
print(f"Checked out connections: {pool.checkedout()}")
print(f"Overflow: {pool.overflow()}")
```

## Environment Configuration

### Required Environment Variables
```bash
# Database connection
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Optional: Async database URL (auto-generated if not provided)
ASYNC_DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name

# Optional: Redis for caching
REDIS_URL=redis://localhost:6379

# Optional: Database pool settings
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
```

### Development vs Production
```python
# Development settings
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/dev_db
DEBUG=True

# Production settings
DATABASE_URL=postgresql://prod_user:secure_pass@prod_host:5432/prod_db
DEBUG=False
SSL_REQUIRE=True
```

This comprehensive guide covers all aspects of database management for the Installment Fraud Detection System. The organized structure and detailed examples make it easy to work with the database layer effectively.