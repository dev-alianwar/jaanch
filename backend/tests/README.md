# Authentication E2E Tests

This directory contains comprehensive end-to-end tests for the authentication system of the Installment Fraud Detection System.

## Test Structure

### Test Files
- `test_auth_e2e.py` - Main authentication tests
- `conftest.py` - Test configuration and fixtures

### Test Classes

#### TestUserRegistration
Tests user registration functionality:
- ✅ Successful customer registration
- ✅ Successful business user registration  
- ✅ Duplicate email handling
- ✅ Invalid email format validation
- ✅ Password length validation
- ✅ Required field validation
- ✅ Role validation

#### TestUserLogin
Tests user login functionality:
- ✅ Successful login
- ✅ Non-existent user handling
- ✅ Wrong password handling
- ✅ Inactive user handling
- ✅ Input validation

#### TestTokenRefresh
Tests JWT token refresh:
- ✅ Successful token refresh
- ✅ Invalid token handling
- ✅ Expired token handling

#### TestAuthenticationFlow
Tests complete authentication workflows:
- ✅ Register → Login flow
- ✅ Login → Access protected endpoint
- ✅ Login → Logout flow

#### TestAuthenticationSecurity
Tests security aspects:
- ✅ Password not returned in responses
- ✅ Email case sensitivity
- ✅ SQL injection protection
- ✅ XSS protection

#### TestRateLimiting
Tests rate limiting functionality:
- ✅ Login attempt rate limiting
- ✅ Registration rate limiting

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