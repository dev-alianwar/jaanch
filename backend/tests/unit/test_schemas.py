"""
Unit tests for Pydantic schemas
"""
import pytest
from pydantic import ValidationError


@pytest.mark.unit
class TestAuthSchemas:
    """Test authentication schemas"""
    
    def test_user_login_schema(self):
        """Test UserLogin schema validation"""
        try:
            from app.schemas.auth import UserLogin
        except ImportError:
            from schemas import UserLogin
        
        # Valid data
        valid_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        login = UserLogin(**valid_data)
        assert login.email == "test@example.com"
        assert login.password == "password123"
        
        # Invalid email
        with pytest.raises(ValidationError):
            UserLogin(email="invalid-email", password="password123")
        
        # Short password
        with pytest.raises(ValidationError):
            UserLogin(email="test@example.com", password="123")
    
    def test_user_register_schema(self):
        """Test UserRegister schema validation"""
        try:
            from app.schemas.auth import UserRegister
            from app.models.user import UserRole
        except ImportError:
            from schemas import UserRegister
            from models import UserRole
        
        # Valid data
        valid_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+1234567890",
            "role": UserRole.CUSTOMER
        }
        
        register = UserRegister(**valid_data)
        assert register.email == "test@example.com"
        assert register.first_name == "Test"
        assert register.role == UserRole.CUSTOMER
        
        # Test default role
        minimal_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        register_minimal = UserRegister(**minimal_data)
        assert register_minimal.role == UserRole.CUSTOMER
        
        # Invalid data
        with pytest.raises(ValidationError):
            UserRegister(
                email="invalid-email",
                password="password123",
                first_name="Test",
                last_name="User"
            )
    
    def test_user_response_schema(self):
        """Test UserResponse schema"""
        try:
            from app.schemas.auth import UserResponse
            from app.models.user import UserRole
        except ImportError:
            from schemas import UserResponse
            from models import UserRole
        
        import uuid
        from datetime import datetime
        
        # Valid data
        valid_data = {
            "id": uuid.uuid4(),
            "email": "test@example.com",
            "role": UserRole.CUSTOMER,
            "first_name": "Test",
            "last_name": "User",
            "phone": "+1234567890",
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        response = UserResponse(**valid_data)
        assert response.email == "test@example.com"
        assert response.role == UserRole.CUSTOMER
        assert response.is_active is True
    
    def test_auth_response_schema(self):
        """Test AuthResponse schema"""
        try:
            from app.schemas.auth import AuthResponse, UserResponse
            from app.models.user import UserRole
        except ImportError:
            from schemas import AuthResponse, UserResponse
            from models import UserRole
        
        import uuid
        from datetime import datetime
        
        # Create user response
        user_data = {
            "id": uuid.uuid4(),
            "email": "test@example.com",
            "role": UserRole.CUSTOMER,
            "first_name": "Test",
            "last_name": "User",
            "phone": None,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        user_response = UserResponse(**user_data)
        
        # Create auth response
        auth_data = {
            "user": user_response,
            "access_token": "fake.jwt.token",
            "refresh_token": "fake.refresh.token",
            "expires_in": 1800
        }
        
        auth_response = AuthResponse(**auth_data)
        assert auth_response.token_type == "bearer"
        assert auth_response.expires_in == 1800
        assert auth_response.user.email == "test@example.com"
    
    def test_token_refresh_schema(self):
        """Test TokenRefresh schema"""
        try:
            from app.schemas.auth import TokenRefresh
        except ImportError:
            from schemas import TokenRefresh
        
        token_data = {"refresh_token": "fake.refresh.token"}
        
        refresh = TokenRefresh(**token_data)
        assert refresh.refresh_token == "fake.refresh.token"
        
        # Test required field
        with pytest.raises(ValidationError):
            TokenRefresh()