"""
Test configuration and fixtures for e2e tests
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import tempfile
from datetime import datetime

# Import our app and dependencies  
from main import app
from database import get_db
from auth import AuthService

# For testing, we'll use the existing PostgreSQL database but with a test schema
# This avoids UUID compatibility issues with SQLite
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/installment_fraud_db")

# Create test engine
engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Import here to avoid circular imports
    from models import User, UserRole
    
    # Create a session
    session = TestingSessionLocal()
    
    # Clean up any existing test data
    session.query(User).filter(User.email.like('%@example.com')).delete()
    session.commit()
    
    yield session
    
    # Clean up test data after test
    session.query(User).filter(User.email.like('%@example.com')).delete()
    session.commit()
    session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+1234567890",
        "role": "customer"
    }

@pytest.fixture
def test_business_user_data():
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
def existing_user(db_session):
    """Create an existing user in the database"""
    user_data = {
        "email": "existing@example.com",
        "password_hash": AuthService.get_password_hash("existingpass123"),
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
    user_data = {
        "email": "inactive@example.com",
        "password_hash": AuthService.get_password_hash("inactivepass123"),
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

@pytest.fixture
def auth_headers(client, existing_user):
    """Get authentication headers for an existing user"""
    login_data = {
        "email": existing_user["user"].email,
        "password": existing_user["password"]
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}