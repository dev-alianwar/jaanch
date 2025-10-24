"""
Test configuration and fixtures for all test types
"""
import pytest
import asyncio
import os
from typing import Generator, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import requests

# Set test environment variables
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/installment_fraud_db")
os.environ.setdefault("JWT_SECRET", "test-secret-key-for-testing")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("LOG_LEVEL", "ERROR")  # Reduce noise in tests

# Test database configuration
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/installment_fraud_db")

# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test"""
    session = TestingSessionLocal()
    
    # Clean up any existing test data
    try:
        # Import here to avoid circular imports
        from models import User
        session.query(User).filter(User.email.like('%@example.com')).delete()
        session.commit()
    except Exception:
        session.rollback()
    
    yield session
    
    # Clean up test data after test
    try:
        from models import User
        session.query(User).filter(User.email.like('%@example.com')).delete()
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


# ============================================================================
# APPLICATION FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def app():
    """Create FastAPI app instance"""
    # Try new modular structure first, fallback to old structure
    try:
        from app.main import app as fastapi_app
        from app.core.database import get_db
        
        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        fastapi_app.dependency_overrides[get_db] = override_get_db
        return fastapi_app
    except ImportError:
        # Fallback to old structure
        from main import app as fastapi_app
        from database import get_db
        
        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        fastapi_app.dependency_overrides[get_db] = override_get_db
        return fastapi_app


@pytest.fixture(scope="function")
def client(app) -> Generator[TestClient, None, None]:
    """Create a test client"""
    with TestClient(app) as test_client:
        yield test_client


# ============================================================================
# USER DATA FIXTURES
# ============================================================================

@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """Sample customer user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "customer"
    }


@pytest.fixture
def test_business_user_data() -> Dict[str, Any]:
    """Sample business user data for testing"""
    return {
        "email": "business@example.com",
        "password": "businesspass123",
        "first_name": "Business",
        "last_name": "Owner",
        "phone": "+1234567891",
        "role": "business"
    }


@pytest.fixture
def test_admin_user_data() -> Dict[str, Any]:
    """Sample admin user data for testing"""
    return {
        "email": "admin@example.com",
        "password": "adminpass123",
        "first_name": "Admin",
        "last_name": "User",
        "phone": "+1234567892",
        "role": "superadmin"
    }


# ============================================================================
# DATABASE USER FIXTURES
# ============================================================================

@pytest.fixture
def existing_user(db_session):
    """Create an existing active user in the database"""
    from database import User, UserRole
    from app.core.security import SecurityService
    
    user_data = {
        "email": "existing@example.com",
        "password_hash": SecurityService.get_password_hash("existingpass123"),
        "first_name": "Existing",
            "last_name": "User",
            "phone": "+1234567892",
            "role": UserRole.CUSTOMER,
            "is_active": True
        }
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return {
        "user": user,
        "password": "existingpass123"
    }


@pytest.fixture
def inactive_user(db_session):
    """Create an inactive user in the database"""
    try:
        from models import User, UserRole
        from auth import AuthService
        
        user_data = {
            "email": "inactive@example.com",
            "password_hash": AuthService.get_password_hash("inactivepass123"),
            "first_name": "Inactive",
            "last_name": "User",
            "phone": "+1234567893",
            "role": UserRole.CUSTOMER,
            "is_active": False
        }
    except ImportError:
        # Try new structure
        from app.models.user import User, UserRole
        from app.core.security import SecurityService
        
        user_data = {
            "email": "inactive@example.com",
            "password_hash": SecurityService.get_password_hash("inactivepass123"),
            "first_name": "Inactive",
            "last_name": "User",
            "phone": "+1234567893",
            "role": UserRole.CUSTOMER,
            "is_active": False
        }
    
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return {
        "user": user,
        "password": "inactivepass123"
    }


# ============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================

@pytest.fixture
def auth_headers(client, existing_user) -> Dict[str, str]:
    """Get authentication headers for an existing user"""
    login_data = {
        "email": existing_user["user"].email,
        "password": existing_user["password"]
    }
    
    # Try new API structure first
    response = client.post("/api/v1/auth/login", json=login_data)
    if response.status_code != 200:
        # Fallback to old structure
        response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# E2E TEST FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def server_url() -> str:
    """Base URL for E2E tests"""
    return os.getenv("TEST_SERVER_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def e2e_session():
    """Session for E2E tests with requests"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session
    session.close()


@pytest.fixture
def e2e_user_data() -> Dict[str, Any]:
    """User data for E2E tests (with unique email)"""
    import uuid
    return {
        "email": f"e2e_test_{uuid.uuid4().hex[:8]}@example.com",
        "password": "e2epassword123",
        "first_name": "E2E",
        "last_name": "Test",
        "phone": "+1234567890",
        "role": "customer"
    }


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def mock_redis():
    """Mock Redis for tests that don't need real Redis"""
    class MockRedis:
        def __init__(self):
            self.data = {}
        
        def get(self, key):
            return self.data.get(key)
        
        def set(self, key, value):
            self.data[key] = value
        
        def setex(self, key, time, value):
            self.data[key] = value
        
        def delete(self, key):
            self.data.pop(key, None)
        
        def ping(self):
            return True
    
    return MockRedis()


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically cleanup test data after each test"""
    yield
    # Cleanup happens in db_session fixture