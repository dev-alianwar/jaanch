"""
Integration tests for database operations
"""
import pytest


@pytest.mark.integration
class TestDatabaseOperations:
    """Test database operations"""
    
    def test_user_crud_operations(self, db_session):
        """Test basic CRUD operations for User model"""
        try:
            from app.models.user import User, UserRole
            from app.core.security import SecurityService
        except ImportError:
            from models import User, UserRole
            from auth import AuthService as SecurityService
        
        # Create
        user = User(
            email="crud_test@example.com",
            password_hash=SecurityService.get_password_hash("testpass123"),
            first_name="CRUD",
            last_name="Test",
            role=UserRole.CUSTOMER,
            is_active=True
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.created_at is not None
        
        # Read
        found_user = db_session.query(User).filter(User.email == "crud_test@example.com").first()
        assert found_user is not None
        assert found_user.email == "crud_test@example.com"
        assert found_user.first_name == "CRUD"
        
        # Update
        found_user.first_name = "Updated"
        db_session.commit()
        
        updated_user = db_session.query(User).filter(User.email == "crud_test@example.com").first()
        assert updated_user.first_name == "Updated"
        
        # Delete
        db_session.delete(updated_user)
        db_session.commit()
        
        deleted_user = db_session.query(User).filter(User.email == "crud_test@example.com").first()
        assert deleted_user is None
    
    def test_user_unique_email_constraint(self, db_session):
        """Test that email uniqueness is enforced"""
        try:
            from app.models.user import User, UserRole
            from app.core.security import SecurityService
        except ImportError:
            from models import User, UserRole
            from auth import AuthService as SecurityService
        
        # Create first user
        user1 = User(
            email="unique_test@example.com",
            password_hash=SecurityService.get_password_hash("testpass123"),
            first_name="First",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        db_session.add(user1)
        db_session.commit()
        
        # Try to create second user with same email
        user2 = User(
            email="unique_test@example.com",
            password_hash=SecurityService.get_password_hash("testpass123"),
            first_name="Second",
            last_name="User",
            role=UserRole.CUSTOMER
        )
        
        db_session.add(user2)
        
        # Should raise an integrity error
        with pytest.raises(Exception):  # Could be IntegrityError or similar
            db_session.commit()
        
        db_session.rollback()
    
    def test_user_role_enum(self, db_session):
        """Test user role enumeration in database"""
        try:
            from app.models.user import User, UserRole
            from app.core.security import SecurityService
        except ImportError:
            from models import User, UserRole
            from auth import AuthService as SecurityService
        
        # Test all role types
        roles_to_test = [UserRole.CUSTOMER, UserRole.BUSINESS, UserRole.SUPERADMIN]
        
        for i, role in enumerate(roles_to_test):
            user = User(
                email=f"role_test_{i}@example.com",
                password_hash=SecurityService.get_password_hash("testpass123"),
                first_name="Role",
                last_name="Test",
                role=role
            )
            
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            
            # Verify role is stored correctly
            found_user = db_session.query(User).filter(User.email == f"role_test_{i}@example.com").first()
            assert found_user.role == role
    
    def test_user_active_inactive_filtering(self, db_session):
        """Test filtering active/inactive users"""
        try:
            from app.models.user import User, UserRole
            from app.core.security import SecurityService
        except ImportError:
            from models import User, UserRole
            from auth import AuthService as SecurityService
        
        # Create active user
        active_user = User(
            email="active_test@example.com",
            password_hash=SecurityService.get_password_hash("testpass123"),
            first_name="Active",
            last_name="User",
            role=UserRole.CUSTOMER,
            is_active=True
        )
        
        # Create inactive user
        inactive_user = User(
            email="inactive_test@example.com",
            password_hash=SecurityService.get_password_hash("testpass123"),
            first_name="Inactive",
            last_name="User",
            role=UserRole.CUSTOMER,
            is_active=False
        )
        
        db_session.add_all([active_user, inactive_user])
        db_session.commit()
        
        # Test filtering
        active_users = db_session.query(User).filter(User.is_active == True).all()
        inactive_users = db_session.query(User).filter(User.is_active == False).all()
        
        active_emails = [u.email for u in active_users]
        inactive_emails = [u.email for u in inactive_users]
        
        assert "active_test@example.com" in active_emails
        assert "inactive_test@example.com" in inactive_emails
        assert "inactive_test@example.com" not in active_emails
        assert "active_test@example.com" not in inactive_emails