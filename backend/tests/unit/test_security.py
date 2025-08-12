"""
Unit tests for security utilities
"""
import pytest
from datetime import datetime, timedelta


@pytest.mark.unit
class TestSecurityService:
    """Test security service functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        try:
            from app.core.security import SecurityService
        except ImportError:
            from auth import AuthService as SecurityService
        
        password = "testpassword123"
        
        # Test hashing
        hashed = SecurityService.get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 20  # Bcrypt hashes are long
        
        # Test verification
        assert SecurityService.verify_password(password, hashed) is True
        assert SecurityService.verify_password("wrongpassword", hashed) is False
    
    def test_jwt_token_creation(self):
        """Test JWT token creation and verification"""
        try:
            from app.core.security import SecurityService
        except ImportError:
            from auth import AuthService as SecurityService
        
        data = {"sub": "test-user-id", "email": "test@example.com"}
        
        # Test access token
        access_token = SecurityService.create_access_token(data)
        assert isinstance(access_token, str)
        assert len(access_token) > 50  # JWT tokens are long
        
        # Test refresh token
        refresh_token = SecurityService.create_refresh_token(data)
        assert isinstance(refresh_token, str)
        assert refresh_token != access_token
    
    def test_jwt_token_verification(self):
        """Test JWT token verification"""
        try:
            from app.core.security import SecurityService
        except ImportError:
            from auth import AuthService as SecurityService
        
        data = {"sub": "test-user-id", "email": "test@example.com"}
        
        # Create and verify access token
        access_token = SecurityService.create_access_token(data)
        payload = SecurityService.verify_token(access_token)
        
        assert payload is not None
        assert payload["sub"] == data["sub"]
        assert payload["type"] == "access"
        
        # Test invalid token
        invalid_payload = SecurityService.verify_token("invalid.token.here")
        assert invalid_payload is None
    
    def test_token_expiration(self):
        """Test token expiration"""
        try:
            from app.core.security import SecurityService
        except ImportError:
            from auth import AuthService as SecurityService
        
        data = {"sub": "test-user-id"}
        
        # Create token with very short expiration
        short_expiry = timedelta(seconds=1)
        token = SecurityService.create_access_token(data, expires_delta=short_expiry)
        
        # Should be valid immediately
        payload = SecurityService.verify_token(token)
        assert payload is not None
        
        # Wait for expiration (in real test, we'd mock time)
        import time
        time.sleep(2)
        
        # Should be invalid after expiration
        expired_payload = SecurityService.verify_token(token)
        assert expired_payload is None