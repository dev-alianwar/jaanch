"""
Unit tests for database models
"""
import pytest
import uuid
from datetime import datetime


@pytest.mark.unit
class TestUserModel:
    """Test User model"""
    
    def test_user_creation(self):
        """Test creating a user instance"""
        try:
            from app.models.user import User, UserRole
        except ImportError:
            from models import User, UserRole
        
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        assert user.email == "test@example.com"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.role == UserRole.CUSTOMER
        assert user.is_active is True  # Default value
    
    def test_user_roles(self):
        """Test user role enumeration"""
        try:
            from app.models.user import UserRole
        except ImportError:
            from models import UserRole
        
        # Test all role values
        assert UserRole.CUSTOMER.value == "customer"
        assert UserRole.BUSINESS.value == "business"
        assert UserRole.SUPERADMIN.value == "superadmin"
        
        # Test role creation
        customer_role = UserRole("customer")
        assert customer_role == UserRole.CUSTOMER
    
    def test_user_representation(self):
        """Test user string representation"""
        try:
            from app.models.user import User, UserRole
        except ImportError:
            from models import User, UserRole
        
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        repr_str = repr(user)
        assert "test@example.com" in repr_str
        assert "customer" in repr_str


@pytest.mark.unit
class TestBaseModel:
    """Test base model functionality"""
    
    def test_base_model_fields(self):
        """Test base model has required fields"""
        try:
            from app.models.user import User, UserRole
        except ImportError:
            from models import User, UserRole
        
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        # Check base fields exist
        assert hasattr(user, 'id')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
        
        # ID should be UUID type
        if hasattr(user, 'id') and user.id:
            assert isinstance(user.id, (str, uuid.UUID))
    
    def test_to_dict_method(self):
        """Test to_dict method if available"""
        try:
            from app.models.user import User, UserRole
        except ImportError:
            from models import User, UserRole
        
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        if hasattr(user, 'to_dict'):
            user_dict = user.to_dict()
            assert isinstance(user_dict, dict)
            assert user_dict['email'] == "test@example.com"
            assert user_dict['first_name'] == "Test"