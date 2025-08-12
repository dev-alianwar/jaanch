# Modular Backend Structure

This document describes the new modular and organized structure for the Installment Fraud Detection System backend.

## Directory Structure

```
backend/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application setup
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration settings
│   │   ├── database.py           # Database setup and session management
│   │   ├── security.py           # Security utilities (JWT, password hashing)
│   │   ├── logging.py            # Logging configuration
│   │   └── exceptions.py         # Custom exceptions
│   ├── models/                   # Database models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model with common fields
│   │   ├── user.py               # User related models
│   │   ├── business.py           # Business models (to be created)
│   │   ├── installment.py        # Installment models (to be created)
│   │   └── fraud.py              # Fraud detection models (to be created)
│   ├── schemas/                  # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── base.py               # Base schema configuration
│   │   ├── auth.py               # Authentication schemas
│   │   ├── user.py               # User schemas (to be created)
│   │   └── installment.py        # Installment schemas (to be created)
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication service
│   │   ├── user.py               # User service (to be created)
│   │   ├── installment.py        # Installment service (to be created)
│   │   └── fraud.py              # Fraud detection service (to be created)
│   └── api/                      # API routes
│       ├── __init__.py
│       ├── dependencies.py       # Common dependencies
│       └── v1/                   # API version 1
│           ├── __init__.py
│           ├── router.py         # Main API router
│           ├── auth.py           # Authentication routes
│           ├── users.py          # User routes (to be created)
│           ├── installments.py   # Installment routes (to be created)
│           └── fraud.py          # Fraud routes (to be created)
├── tests_new/                    # Tests for new structure
│   ├── __init__.py
│   ├── conftest.py               # Test configuration
│   └── test_auth_modular.py      # Authentication tests
├── main_new.py                   # Application entry point
├── test_modular.py               # Simple test runner
└── requirements.txt              # Dependencies
```

## Key Features

### 1. Separation of Concerns
- **Models**: Database models with SQLAlchemy
- **Schemas**: Pydantic models for API validation
- **Services**: Business logic layer
- **API**: Route handlers with minimal logic

### 2. Configuration Management
- Centralized configuration in `app/core/config.py`
- Environment-based settings with Pydantic
- Type-safe configuration with validation

### 3. Security
- JWT token management in `app/core/security.py`
- Password hashing utilities
- Role-based access control

### 4. Database
- Base model with common fields (id, created_at, updated_at)
- Proper session management
- Migration support with Alembic

### 5. API Versioning
- Versioned API routes (`/api/v1/`)
- Backward compatibility support
- Clear API structure

### 6. Error Handling
- Custom exception classes
- Global exception handlers
- Consistent error responses

### 7. Logging
- Structured logging configuration
- Per-module loggers
- Configurable log levels

## Running the New Structure

### 1. Start the Server
```bash
cd backend
python3 main_new.py
```

### 2. Test the API
```bash
# Simple test runner
python3 test_modular.py

# Or use pytest
python3 -m pytest tests_new/ -v
```

### 3. API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## Migration from Old Structure

### Completed
- ✅ Core configuration and database setup
- ✅ Authentication system (register, login, token refresh)
- ✅ User models and schemas
- ✅ Security utilities
- ✅ Basic API structure
- ✅ Error handling
- ✅ Logging setup

### To Be Migrated
- [ ] Business models and services
- [ ] Installment system
- [ ] Fraud detection engine
- [ ] Admin functionality
- [ ] Translation system
- [ ] Reporting services

## Benefits of New Structure

### 1. Maintainability
- Clear separation of concerns
- Easy to locate and modify code
- Consistent patterns across modules

### 2. Testability
- Isolated business logic in services
- Easy to mock dependencies
- Clear test structure

### 3. Scalability
- Modular architecture supports growth
- Easy to add new features
- Independent module development

### 4. Code Quality
- Type hints throughout
- Consistent error handling
- Proper logging

### 5. Developer Experience
- Clear project structure
- Easy onboarding for new developers
- Good documentation

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Token refresh
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user

### Health
- `GET /health` - Health check
- `GET /` - Root endpoint

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Security
JWT_SECRET=your-secret-key
JWT_EXPIRE_MINUTES=30

# Redis (optional)
REDIS_URL=redis://localhost:6379

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
```

## Testing

### Unit Tests
```bash
python3 -m pytest tests_new/test_auth_modular.py -v
```

### Integration Tests
```bash
python3 test_modular.py
```

### Test Coverage
```bash
python3 -m pytest tests_new/ --cov=app --cov-report=html
```

## Next Steps

1. **Migrate remaining modules** to the new structure
2. **Add comprehensive tests** for all modules
3. **Implement API documentation** with examples
4. **Add monitoring and metrics**
5. **Set up CI/CD pipeline**
6. **Performance optimization**

This modular structure provides a solid foundation for scaling the application while maintaining code quality and developer productivity.