# Comprehensive Test Suite

This directory contains all tests for the Installment Fraud Detection System backend, organized by test type.

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared test configuration and fixtures
├── README.md                      # This file
├── test_auth_e2e.py              # Legacy E2E tests (kept for compatibility)
├── unit/                         # Unit tests - fast, isolated
│   ├── __init__.py
│   ├── test_security.py          # Security utilities tests
│   ├── test_models.py            # Database model tests
│   └── test_schemas.py           # Pydantic schema tests
├── integration/                  # Integration tests - component interactions
│   ├── __init__.py
│   ├── test_auth_service.py      # Authentication service tests
│   ├── test_auth_modular.py      # Modular structure auth tests
│   └── test_database.py          # Database operation tests
└── e2e/                         # End-to-end tests - full workflows
    ├── __init__.py
    └── test_auth_flow.py         # Complete authentication flows
```

## Test Types

### Unit Tests (`tests/unit/`)
Fast, isolated tests that test individual components:
- **Security utilities**: Password hashing, JWT tokens
- **Database models**: Model creation, validation, relationships
- **Pydantic schemas**: Input validation, serialization

### Integration Tests (`tests/integration/`)
Tests that verify component interactions:
- **Authentication service**: Business logic with database
- **Database operations**: CRUD operations, constraints
- **API endpoints**: Route handlers with dependencies

### End-to-End Tests (`tests/e2e/`)
Complete workflow tests that simulate real user interactions:
- **Authentication flows**: Registration → Login → Protected access
- **Token management**: Refresh, logout workflows
- **Error scenarios**: Invalid credentials, duplicate registration

## Test Categories (Markers)

Tests are marked with pytest markers for easy filtering:

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests  
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.auth` - Authentication related tests
- `@pytest.mark.database` - Database related tests
- `@pytest.mark.slow` - Slow running tests

## Running Tests

### Install Dependencies
```bash
pip install -r requirements-test.txt
```

### Run All Authentication Tests
```bash
pytest tests/test_auth_e2e.py -v
```

### Run Specific Test Classes
```bash
# Registration tests only
pytest tests/test_auth_e2e.py::TestUserRegistration -v

# Login tests only
pytest tests/test_auth_e2e.py::TestUserLogin -v

# Security tests only
pytest tests/test_auth_e2e.py::TestAuthenticationSecurity -v
```

### Run with Coverage
```bash
pytest tests/test_auth_e2e.py --cov=. --cov-report=html
```

### Quick Test Runner
```bash
python test_auth_quick.py
```

### Full Test Suite
```bash
python run_tests.py
```

## Test Database

Tests use an isolated SQLite database that is created and destroyed for each test function. This ensures:
- No interference between tests
- Fast test execution
- No dependency on external databases during testing

## Fixtures

### Available Fixtures
- `client` - FastAPI test client
- `db_session` - Database session for each test
- `test_user_data` - Sample customer user data
- `test_business_user_data` - Sample business user data
- `existing_user` - Pre-created active user
- `inactive_user` - Pre-created inactive user
- `auth_headers` - Authentication headers for API calls

## Expected HTTP Status Codes

### Registration
- `201 CREATED` - Successful registration
- `400 BAD REQUEST` - Duplicate email, business logic errors
- `422 UNPROCESSABLE_ENTITY` - Validation errors

### Login
- `200 OK` - Successful login
- `401 UNAUTHORIZED` - Invalid credentials, inactive user
- `422 UNPROCESSABLE_ENTITY` - Validation errors
- `429 TOO_MANY_REQUESTS` - Rate limiting

### Token Refresh
- `200 OK` - Successful refresh
- `401 UNAUTHORIZED` - Invalid/expired refresh token

## Test Data

### Sample User Data
```json
{
  "email": "test@example.com",
  "password": "testpassword123",
  "first_name": "Test",
  "last_name": "User",
  "phone": "+1234567890",
  "role": "customer"
}
```

### Sample Business User Data
```json
{
  "email": "business@example.com",
  "password": "businesspass123",
  "first_name": "Business",
  "last_name": "Owner",
  "phone": "+1234567891",
  "role": "business"
}
```

## Security Test Cases

The tests include comprehensive security validations:

1. **Input Validation**: Email format, password strength, required fields
2. **Authentication**: Correct credential verification
3. **Authorization**: Role-based access control
4. **Data Protection**: Passwords never returned in responses
5. **Injection Protection**: SQL injection and XSS prevention
6. **Rate Limiting**: Brute force attack prevention

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 30 seconds for full suite)
- No external dependencies
- Clear pass/fail indicators
- Detailed error reporting

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Errors**: Check SQLAlchemy models are properly imported
3. **Token Errors**: Verify JWT configuration in test environment
4. **Rate Limiting**: Tests may fail if Redis is required but not available

### Debug Mode
Run tests with verbose output:
```bash
pytest tests/test_auth_e2e.py -v -s --tb=long
```
## Run
ning Tests

### Install Dependencies
```bash
pip install -r requirements-test.txt
```

### Run All Tests
```bash
# Run comprehensive test suite
python3 run_all_tests.py

# Or use pytest directly
python3 -m pytest tests/ -v
```

### Run Specific Test Types
```bash
# Unit tests only (fast)
python3 -m pytest tests/unit/ -v
python3 run_all_tests.py --type unit

# Integration tests only
python3 -m pytest tests/integration/ -v
python3 run_all_tests.py --type integration

# E2E tests only
python3 -m pytest tests/e2e/ -v
python3 run_all_tests.py --type e2e
```

### Run Tests by Category
```bash
# Authentication tests only
python3 -m pytest -m auth -v

# Database tests only
python3 -m pytest -m database -v

# Skip slow tests
python3 -m pytest -m "not slow" -v
python3 run_all_tests.py --fast
```

### Run with Coverage
```bash
# Coverage report
python3 -m pytest --cov=app --cov-report=html
python3 run_all_tests.py --coverage

# View coverage report
open htmlcov/index.html
```

## Test Configuration

### Environment Variables
Tests use these environment variables (with defaults):
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/installment_fraud_db
JWT_SECRET=test-secret-key-for-testing
DEBUG=true
LOG_LEVEL=ERROR
```

### Test Database
- Uses the same PostgreSQL database as development
- Automatically cleans up test data after each test
- Test users have emails ending with `@example.com`

### Fixtures Available
- `client` - FastAPI test client
- `db_session` - Database session
- `test_user_data` - Sample user data
- `existing_user` - Pre-created user in database
- `auth_headers` - Authentication headers
- `e2e_session` - Requests session for E2E tests

## Writing New Tests

### Unit Test Example
```python
import pytest

@pytest.mark.unit
class TestMyComponent:
    def test_my_function(self):
        # Test individual function
        result = my_function("input")
        assert result == "expected"
```

### Integration Test Example
```python
import pytest

@pytest.mark.integration
class TestMyService:
    def test_service_with_database(self, db_session):
        # Test service with database
        service = MyService(db_session)
        result = service.create_item(data)
        assert result.id is not None
```

### E2E Test Example
```python
import pytest

@pytest.mark.e2e
class TestMyWorkflow:
    def test_complete_workflow(self, server_url, e2e_session):
        # Test complete user workflow
        response = e2e_session.post(f"{server_url}/api/endpoint")
        assert response.status_code == 200
```

## Test Data Management

### Cleanup Strategy
- Each test gets a fresh database session
- Test data is automatically cleaned up after each test
- Uses email pattern `*@example.com` for easy identification

### Test User Creation
```python
def test_with_user(self, db_session):
    user = User(email="test@example.com", ...)
    db_session.add(user)
    db_session.commit()
    # Test will automatically clean up
```

## Continuous Integration

Tests are designed for CI/CD:
- Fast execution (unit tests < 5s, integration < 30s)
- Reliable cleanup
- Clear pass/fail indicators
- Detailed error reporting

## Troubleshooting

### Common Issues
1. **Database connection**: Ensure PostgreSQL is running
2. **Import errors**: Check Python path and dependencies
3. **Test isolation**: Each test should be independent

### Debug Commands
```bash
# Verbose output with full traceback
python3 -m pytest tests/ -v -s --tb=long

# Run single test
python3 -m pytest tests/unit/test_security.py::TestSecurityService::test_password_hashing -v

# Debug with pdb
python3 -m pytest tests/ --pdb
```

### Performance
```bash
# Show slowest tests
python3 -m pytest tests/ --durations=10

# Profile test execution
python3 -m pytest tests/ --profile
```

This organized structure makes it easy to:
- Find the right type of test to write
- Run specific test categories
- Maintain test isolation
- Scale the test suite as the application grows