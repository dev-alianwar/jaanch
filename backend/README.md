# Backend - Installment Fraud Detection System

FastAPI backend for the Installment Fraud Detection System with PostgreSQL database, JWT authentication, and modular architecture.

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI (Python 3.8+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Caching**: Redis (optional)
- **Testing**: Pytest with comprehensive test coverage
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### Project Structure
```
backend/
├── main.py                     # Application entry point
├── pytest.ini                 # Test configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                 # Container configuration
│
├── app/                       # Main application package
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database setup
│   │   ├── security.py        # Security utilities
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── logging.py         # Logging configuration
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py           # Authentication schemas
│   │   ├── installment.py    # Installment schemas
│   │   └── history.py        # History schemas
│   ├── services/              # Business logic layer
│   └── api/                   # API routes
│       └── v1/                # API version 1
│           ├── router.py      # Main API router
│           └── modules/       # Feature modules
│               ├── auth/      # Authentication
│               ├── installments/ # Installment management
│               ├── history/   # Customer history
│               ├── admin/     # Admin functions
│               ├── approval/  # Approval workflows
│               ├── fraud/     # Fraud detection
│               ├── users/     # User management
│               └── translation/ # Multi-language
│
├── database/                  # Database package
│   ├── database.py           # Connection management
│   ├── database_utils.py     # Database utilities
│   ├── models.py             # SQLAlchemy models
│   ├── init.sql              # Database initialization
│   ├── alembic.ini           # Migration configuration
│   ├── COMPLETE_DATABASE_GUIDE.md # Database documentation
│   └── migrations/           # Database migrations
│
├── tests/                    # Test suite
│   ├── conftest.py          # Test configuration
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
│
└── scripts/                 # Utility scripts
    ├── run_all_tests.py    # Test runner
    ├── verify_*.py         # Structure verification
    └── SCRIPTS_GUIDE.md    # Scripts documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)

### Installation

1. **Clone and Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Database Setup**
   ```bash
   # Initialize database
   python -c "from database.database_utils import init_database; init_database()"
   
   # Run migrations (optional)
   cd database && alembic upgrade head
   ```

4. **Start Application**
   ```bash
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Verify Installation**
   ```bash
   # Run tests
   python scripts/run_all_tests.py
   
   # Check structure
   python scripts/verify_clean_structure.py
   
   # Access API docs
   curl http://localhost:8000/docs
   ```

### Docker Setup (Recommended)
```bash
# Build and start
docker-compose up --build

# Run tests in container
docker-compose exec backend python scripts/run_all_tests.py
```

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/auth/me` - Get current user info

### Installments
- `GET /api/v1/installments/businesses` - List businesses
- `POST /api/v1/installments/requests` - Create installment request
- `GET /api/v1/installments/requests` - List requests (paginated)
- `PUT /api/v1/installments/requests/{id}` - Update request

### History & Analytics
- `GET /api/v1/history/customer/{id}` - Customer installment history
- `GET /api/v1/history/my-history` - Personal history
- `GET /api/v1/history/active-plans` - Active installment plans

### Admin & Fraud Detection
- `GET /api/v1/admin/dashboard` - Admin dashboard data
- `GET /api/v1/fraud/alerts` - Fraud alerts
- `POST /api/v1/fraud/analyze/{customer_id}` - Analyze customer risk

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🗄️ Database

### Models
- **User**: All user accounts (customers, businesses, admins)
- **Business**: Business information and verification
- **InstallmentRequest**: Customer purchase requests
- **InstallmentPlan**: Approved payment plans
- **Payment**: Individual payment records
- **FraudAlert**: Fraud detection alerts
- **FraudPattern**: Pattern analysis results

### Key Features
- UUID primary keys for security
- Automatic timestamps (created_at, updated_at)
- Proper foreign key relationships
- Strategic indexes for performance
- JSON fields for flexible metadata

### Migration Commands
```bash
cd database

# Check current status
alembic current

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🧪 Testing

### Test Organization
- **Unit Tests** (`tests/unit/`): Fast, isolated component tests
- **Integration Tests** (`tests/integration/`): Component interaction tests
- **End-to-End Tests** (`tests/e2e/`): Complete workflow tests

### Running Tests
```bash
# All tests
python scripts/run_all_tests.py

# Specific test types
python scripts/run_all_tests.py --type unit
python scripts/run_all_tests.py --type integration
python scripts/run_all_tests.py --type e2e

# With coverage
python scripts/run_all_tests.py --coverage

# Specific categories
python -m pytest -m auth -v      # Authentication tests
python -m pytest -m database -v  # Database tests
```

### Test Configuration
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short --cov=app --cov-report=term-missing
markers =
    unit: Unit tests - fast, isolated tests
    integration: Integration tests - component interactions
    e2e: End-to-end tests - full workflow tests
    auth: Authentication related tests
    database: Database related tests
```

## 🔧 Development

### Code Structure
Each API module follows this pattern:
```
module_name/
├── __init__.py
├── module_name_routes.py    # FastAPI routes
├── module_name_service.py   # Business logic
└── module_name_models.py    # Additional models (optional)
```

### Adding New Modules
1. Create module directory in `app/api/v1/modules/`
2. Implement routes and service files
3. Add to main router in `app/api/v1/router.py`
4. Create corresponding tests
5. Update documentation

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Security
JWT_SECRET=your-secret-key
JWT_EXPIRE_MINUTES=30

# Optional
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=["http://localhost:3000"]
LOG_LEVEL=INFO
```

### Useful Commands
```bash
# Development
python main.py                          # Start server
python scripts/debug_auth.py            # Debug authentication
python scripts/test_modular.py          # Test modular structure

# Database
python -c "from database.database_utils import check_database_connection; print(check_database_connection())"
python database/database_utils.py       # Test DB connection

# Structure Verification
python scripts/verify_clean_structure.py     # Overall structure
python scripts/verify_database_structure.py  # Database structure
python scripts/verify_modular_structure.py   # API modules
python scripts/verify_test_structure.py      # Test organization
```

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (superadmin, business, customer)
- Password hashing with bcrypt
- Session management with Redis (optional)

### Data Protection
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic schemas
- CORS configuration for web security
- Encrypted sensitive data storage

### API Security
- Rate limiting (configurable)
- Request/response validation
- Comprehensive error handling
- Audit logging for sensitive operations

## 📊 Fraud Detection

### Detection Algorithms
- **Rapid Requests**: Multiple requests in short timeframe
- **High Debt Ratio**: Total debt exceeding thresholds
- **Cross-Business Chains**: Installment patterns across businesses
- **Payment Defaults**: Historical payment failure patterns

### Risk Scoring
- Customer risk scores (0.0 - 1.0)
- Configurable thresholds
- Real-time risk calculation
- Historical pattern analysis

### Alerts & Monitoring
- Automated fraud alerts
- Severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Alert status tracking
- Investigation workflows

## 🚨 Troubleshooting

### Common Issues

**Database Connection**
```bash
# Check connection
python -c "from database.database_utils import check_database_connection; print(check_database_connection())"

# Verify environment
echo $DATABASE_URL
```

**Import Errors**
```bash
# Verify structure
python scripts/verify_clean_structure.py

# Check Python path
python -c "import sys; print(sys.path)"
```

**Test Failures**
```bash
# Run specific test with verbose output
python -m pytest tests/unit/test_security.py::test_password_hashing -v -s

# Debug mode
python -m pytest tests/unit/test_security.py -v -s --tb=long
```

**Server Issues**
```bash
# Check server health
curl http://localhost:8000/health

# View logs
tail -f logs/app.log

# Debug authentication
python scripts/debug_auth.py
```

## 📈 Performance

### Database Optimization
- Connection pooling (20 connections, 30 overflow)
- Strategic indexes on frequently queried columns
- Query optimization with SQLAlchemy
- Connection recycling (1 hour)

### Caching Strategy
- Redis for session storage
- API response caching (configurable)
- Database query result caching
- Static asset caching

### Monitoring
```python
# Connection pool status
from database import engine
pool = engine.pool
print(f"Pool size: {pool.size()}")
print(f"Checked out: {pool.checkedout()}")
```

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Write tests for new functionality
3. Update documentation for API changes
4. Run verification scripts before committing
5. Use type hints throughout the codebase

### Code Quality
- Type hints with mypy
- Code formatting with black
- Import sorting with isort
- Linting with flake8
- Security scanning with bandit

This backend provides a robust, scalable foundation for the Installment Fraud Detection System with comprehensive fraud detection capabilities, clean architecture, and extensive testing.