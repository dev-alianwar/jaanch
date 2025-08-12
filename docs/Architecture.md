# Installment Fraud Detection System - Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Backend Structure](#backend-structure)
4. [Database Design](#database-design)
5. [API Structure](#api-structure)
6. [Testing Strategy](#testing-strategy)
7. [Requirements](#requirements)
8. [Quick Start Guide](#quick-start-guide)

## System Overview

The Installment Fraud Detection System is a comprehensive platform that tracks installment purchases across multiple businesses to detect and prevent fraudulent chains. The system uses a multi-tenant architecture with role-based access control, real-time fraud detection algorithms, and cross-business data sharing capabilities.

### Key Features
- **Multi-platform Access**: Pure React Native mobile app, Next.js web platform, and FastAPI backend
- **Role-based Access Control**: Superadmin, business, and customer roles
- **Cross-business Fraud Detection**: Track installment chains across multiple businesses
- **Real-time Analytics**: Comprehensive reporting and fraud pattern detection
- **Secure Architecture**: JWT authentication, encrypted data, audit trails

## Architecture

### System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Mobile App     │    │  Web Platform   │    │  Backend API    │
│  (React Native)│◄──►│  (Next.js)      │◄──►│  (FastAPI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                               ┌─────────────────┐
                                               │  Database       │
                                               │  (PostgreSQL)   │
                                               └─────────────────┘
```

### Technology Stack
- **Backend**: FastAPI (Python), PostgreSQL, Redis
- **Web**: Next.js (TypeScript), Tailwind CSS
- **Mobile**: Pure React Native (TypeScript)
- **Infrastructure**: Docker, Docker Compose

## Backend Structure

### Clean Directory Organization
```
backend/
├── main.py                     # Application entry point
├── pytest.ini                 # Test configuration
├── requirements.txt            # Dependencies
├── Dockerfile                 # Container configuration
│
├── app/                       # Main application package
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database setup
│   │   ├── security.py        # Security utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py           # Authentication schemas
│   │   ├── installment.py    # Installment schemas
│   │   └── history.py        # History schemas
│   ├── services/              # Business logic layer
│   └── api/                   # API routes
│       └── v1/                # API version 1
│           ├── router.py      # Main API router
│           └── modules/       # Feature modules
│               ├── auth/      # Authentication module
│               ├── installments/ # Installments module
│               ├── history/   # History module
│               ├── admin/     # Admin module
│               ├── approval/  # Approval module
│               ├── fraud/     # Fraud detection module
│               ├── users/     # User management
│               └── translation/ # Multi-language support
│
├── database/                  # Database package
│   ├── database.py           # Connection management
│   ├── database_utils.py     # Database utilities
│   ├── models.py             # SQLAlchemy models
│   ├── init.sql              # Database initialization
│   ├── alembic.ini           # Migration configuration
│   └── migrations/           # Database migrations
│
├── tests/                    # Organized test structure
│   ├── conftest.py          # Test configuration
│   ├── unit/                # Unit tests (fast, isolated)
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
│
├── scripts/                 # Utility scripts
│   ├── run_all_tests.py    # Comprehensive test runner
│   ├── verify_*.py         # Structure verification scripts
│   └── debug_*.py          # Debugging utilities
│
└── docs/                   # Documentation
    └── [this file]
```

### Module Structure Pattern
Each API module follows this consistent pattern:
```
module_name/
├── __init__.py
├── module_name_routes.py    # FastAPI routes
└── module_name_service.py   # Business logic
```

## Database Design

### Core Models
- **User**: All user accounts (customers, businesses, admins)
- **Business**: Business information and verification
- **InstallmentRequest**: Purchase requests from customers
- **InstallmentPlan**: Approved payment plans
- **Payment**: Individual payment records
- **FraudAlert**: Detected suspicious activities
- **FraudPattern**: Pattern analysis results

### Key Enums
- **UserRole**: SUPERADMIN, BUSINESS, CUSTOMER
- **RequestStatus**: PENDING, APPROVED, REJECTED
- **PlanStatus**: ACTIVE, COMPLETED, DEFAULTED, CANCELLED
- **AlertType**: RAPID_REQUESTS, HIGH_DEBT_RATIO, CROSS_BUSINESS_CHAIN

### Database Features
- UUID primary keys for security
- Automatic timestamps (created_at, updated_at)
- Proper foreign key relationships
- Indexes on frequently queried columns
- JSON fields for flexible metadata storage

## API Structure

### Authentication Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `GET /api/v1/auth/me` - Get current user info

### Installment Endpoints
- `GET /api/v1/installments/businesses` - List businesses
- `POST /api/v1/installments/requests` - Create request
- `GET /api/v1/installments/requests` - List requests (paginated)
- `PUT /api/v1/installments/requests/{id}` - Update request

### History Endpoints
- `GET /api/v1/history/customer/{id}` - Customer history
- `GET /api/v1/history/my-history` - Personal history
- `GET /api/v1/history/active-plans` - Active plans

### API Features
- JWT-based authentication
- Role-based authorization
- Request/response validation with Pydantic
- Comprehensive error handling
- API documentation with OpenAPI/Swagger

## Testing Strategy

### Test Organization
- **Unit Tests** (tests/unit/): Fast, isolated component tests
- **Integration Tests** (tests/integration/): Component interaction tests
- **End-to-End Tests** (tests/e2e/): Complete workflow tests

### Test Categories
- **Authentication Tests**: Login, registration, token management
- **Database Tests**: CRUD operations, model validation
- **API Tests**: Endpoint functionality, error handling
- **Security Tests**: Authorization, input validation

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

### Running Tests
```bash
# All tests
python3 scripts/run_all_tests.py

# By type
python3 -m pytest tests/unit/ -v
python3 -m pytest tests/integration/ -v
python3 -m pytest tests/e2e/ -v

# By category
python3 -m pytest -m auth -v
python3 -m pytest -m database -v

# With coverage
python3 scripts/run_all_tests.py --coverage
```

## Requirements

### Functional Requirements

#### R1: User Authentication and Role Management
- Multi-role authentication (superadmin, business, customer)
- JWT-based session management
- Role-based access control

#### R2: Customer Installment Request Management
- Business selection interface
- Product installment request creation
- Request status tracking

#### R3: Business Request Management
- Installment request approval/rejection
- Customer history visibility
- Business dashboard

#### R4: Cross-Business History Visibility
- Complete customer installment history
- Cross-business data sharing
- Risk assessment information

#### R5: Fraud Detection and Chain Tracking
- Pattern detection algorithms
- Multi-business installment tracking
- Automated fraud alerts
- Risk score calculation

#### R6: Superadmin Oversight
- System-wide analytics
- Fraud monitoring dashboard
- Business management
- Configuration management

#### R7: Multi-Platform Access
- Pure React Native mobile app
- Next.js web platform with landing page
- Responsive design
- Cross-platform data synchronization

### Technical Requirements
- **Security**: HTTPS, JWT tokens, password hashing, SQL injection protection
- **Performance**: Database indexing, connection pooling, caching with Redis
- **Scalability**: Modular architecture, horizontal scaling support
- **Reliability**: Error handling, logging, automated testing
- **Maintainability**: Clean code structure, comprehensive documentation

## Quick Start Guide

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Docker & Docker Compose (recommended)

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd backend
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
   python3 -c "from database.database_utils import init_database; init_database()"
   
   # Run migrations
   cd database && alembic upgrade head
   ```

4. **Start Application**
   ```bash
   python3 main.py
   ```

5. **Verify Installation**
   ```bash
   # Run tests
   python3 scripts/run_all_tests.py
   
   # Check structure
   python3 scripts/verify_clean_structure.py
   
   # Access API docs
   curl http://localhost:8000/docs
   ```

### Docker Setup (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Run tests in container
docker-compose exec backend python3 scripts/run_all_tests.py
```

### Development Workflow

1. **Make Changes**
   - Edit code in appropriate module
   - Follow existing patterns and structure

2. **Test Changes**
   ```bash
   # Run relevant tests
   python3 -m pytest tests/unit/test_your_module.py -v
   
   # Run all tests
   python3 scripts/run_all_tests.py
   ```

3. **Verify Structure**
   ```bash
   python3 scripts/verify_clean_structure.py
   ```

4. **Update Documentation**
   - Update this file if architecture changes
   - Add API documentation for new endpoints

### Useful Commands

```bash
# Development
python3 main.py                          # Start server
python3 scripts/debug_auth.py            # Debug authentication
python3 scripts/test_modular.py          # Test modular structure

# Testing
python3 scripts/run_all_tests.py         # All tests
python3 scripts/run_all_tests.py --type unit  # Unit tests only
python3 -m pytest -m auth -v             # Auth tests only

# Database
python3 database/database_utils.py       # Test DB connection
cd database && alembic current           # Check migrations
cd database && alembic revision --autogenerate -m "Description"

# Structure Verification
python3 scripts/verify_clean_structure.py     # Overall structure
python3 scripts/verify_database_structure.py  # Database structure
python3 scripts/verify_modular_structure.py   # API modules
python3 scripts/verify_test_structure.py      # Test organization
```

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Troubleshooting

**Database Connection Issues**
```bash
# Check connection
python3 -c "from database.database_utils import check_database_connection; print(check_database_connection())"

# Reset database
python3 -c "from database.database_utils import init_database; init_database()"
```

**Import Errors**
```bash
# Verify structure
python3 scripts/verify_clean_structure.py

# Check Python path
python3 -c "import sys; print(sys.path)"
```

**Test Failures**
```bash
# Run specific test
python3 -m pytest tests/unit/test_security.py::test_password_hashing -v

# Debug mode
python3 -m pytest tests/unit/test_security.py -v -s --tb=long
```

This consolidated documentation provides a complete overview of the system architecture, structure, and usage. The clean, modular organization makes the codebase maintainable and scalable while providing comprehensive testing and documentation.