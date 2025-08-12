"""
Integration tests for authentication service
"""
import pytest
from fastapi import HTTPException


@pytest.mark.integration
class TestAuthService:
    """Test authentication service with database"""
    
    def test_register_user_success(self, db_session):
        """Test successful user registration"""
        try:
            from app.services.auth import AuthService
            from app.schemas.auth import UserRegister
            from app.models.user import UserRole
        except ImportError:
            pytest.skip("New modular structure not available")
        
        user_data = UserRegister(
            email="integration_test@example.com",
            password="testpass123",
            first_name="Integration",
            last_name="Test",
            role=UserRole.CUSTOMER
        )
        
        result = AuthService.register_user(db_session, user_data)
        
        assert result.user.email == "integration_test@example.com"
        assert result.user.first_name == "Integration"
        assert result.user.role == UserRole.CUSTOMER
        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"
    
    def test_register_duplicate_email(self, db_session, existing_user):
        """Test registration with duplicate email"""
        try:
            from app.services.auth import AuthService
            from app.schemas.auth import UserRegister
            from app.models.user import UserRole
        except ImportError:
            pytest.skip("New modular structure not available")
        
        user_data = UserRegister(
            email=existing_user["user"].email,
            password="testpass123",
            first_name="Duplicate",
            last_name="Test",
            role=UserRole.CUSTOMER
        )
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.register_user(db_session, user_data)
        
        assert exc_info.value.status_code == 400
        assert "already registered" in exc_info.value.detail.lower()
    
    def test_authenticate_user_success(self, db_session, existing_user):
        """Test successful user authentication"""
        try:
            from app.services.auth import AuthService
        except ImportError:
            pytest.skip("New modular structure not available")
        
        user = AuthService.authenticate_user(
            db_session,
            existing_user["user"].email,
            existing_user["password"]
        )
        
        assert user is not None
        assert user.email == existing_user["user"].email
        assert user.is_active is True
    
    def test_authenticate_user_wrong_password(self, db_session, existing_user):
        """Test authentication with wrong password"""
        try:
            from app.services.auth import AuthService
        except ImportError:
            pytest.skip("New modular structure not available")
        
        user = AuthService.authenticate_user(
            db_session,
            existing_user["user"].email,
            "wrongpassword"
        )
        
        assert user is None
    
    def test_authenticate_nonexistent_user(self, db_session):
        """Test authentication with non-existent user"""
        try:
            from app.services.auth import AuthService
        except ImportError:
            pytest.skip("New modular structure not available")
        
        user = AuthService.authenticate_user(
            db_session,
            "nonexistent@example.com",
            "somepassword"
        )
        
        assert user is None
    
    def test_login_user_success(self, db_session, existing_user):
        """Test successful user login"""
        try:
            from app.services.auth import AuthService
            from app.schemas.auth import UserLogin
        except ImportError:
            pytest.skip("New modular structure not available")
        
        login_data = UserLogin(
            email=existing_user["user"].email,
            password=existing_user["password"]
        )
        
        result = AuthService.login_user(db_session, login_data)
        
        assert result.user.email == existing_user["user"].email
        assert result.access_token is not None
        assert result.refresh_token is not None
    
    def test_login_user_invalid_credentials(self, db_session):
        """Test login with invalid credentials"""
        try:
            from app.services.auth import AuthService
            from app.schemas.auth import UserLogin
        except ImportError:
            pytest.skip("New modular structure not available")
        
        login_data = UserLogin(
            email="nonexistent@example.com",
            password="wrongpassword"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.login_user(db_session, login_data)
        
        assert exc_info.value.status_code == 401
    
    def test_refresh_token_success(self, db_session, existing_user):
        """Test successful token refresh"""
        try:
            from app.services.auth import AuthService
            from app.schemas.auth import UserLogin
        except ImportError:
            pytest.skip("New modular structure not available")
        
        # First login to get refresh token
        login_data = UserLogin(
            email=existing_user["user"].email,
            password=existing_user["password"]
        )
        
        login_result = AuthService.login_user(db_session, login_data)
        refresh_token = login_result.refresh_token
        
        # Use refresh token to get new tokens
        refresh_result = AuthService.refresh_token(db_session, refresh_token)
        
        assert refresh_result.user.email == existing_user["user"].email
        assert refresh_result.access_token != login_result.access_token
        assert refresh_result.refresh_token != refresh_token
    
    def test_refresh_token_invalid(self, db_session):
        """Test refresh with invalid token"""
        try:
            from app.services.auth import AuthService
        except ImportError:
            pytest.skip("New modular structure not available")
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.refresh_token(db_session, "invalid.token.here")
        
        assert exc_info.value.status_code == 401