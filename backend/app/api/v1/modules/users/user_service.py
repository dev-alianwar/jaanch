"""
User management service layer for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import logging

from models import User, Business, UserRole
from auth import AuthService
from schemas import UserRegister, BusinessCreate

logger = logging.getLogger(__name__)

class UserService:
    """Service class for user management operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """Create a new user"""
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create new user
        hashed_password = AuthService.get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            role=user_data.role,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"User created: {new_user.email} with role {new_user.role}")
        return new_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users_paginated(
        db: Session,
        page: int = 1,
        size: int = 10,
        role: Optional[UserRole] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Tuple[List[User], int]:
        """Get paginated list of users with filters"""
        
        query = db.query(User)
        
        # Apply filters
        if role:
            query = query.filter(User.role == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if search:
            search_filter = or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        users = query.offset(offset).limit(size).all()
        
        return users, total
    
    @staticmethod
    def update_user(db: Session, user_id: str, update_data: Dict[str, Any]) -> Optional[User]:
        """Update user information"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Update allowed fields
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        logger.info(f"User updated: {user.email}")
        return user
    
    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> bool:
        """Deactivate user"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Prevent deactivating superadmin users
        if user.role == UserRole.SUPERADMIN:
            raise ValueError("Cannot deactivate superadmin users")
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"User deactivated: {user.email}")
        return True
    
    @staticmethod
    def activate_user(db: Session, user_id: str) -> bool:
        """Activate user"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"User activated: {user.email}")
        return True
    
    @staticmethod
    def get_user_statistics(db: Session) -> Dict[str, Any]:
        """Get user statistics"""
        
        # Get user counts by role
        user_stats = db.query(
            User.role,
            func.count(User.id).label('count'),
            func.count(func.nullif(User.is_active, False)).label('active_count')
        ).group_by(User.role).all()
        
        # Format response
        role_stats = {}
        total_users = 0
        total_active = 0
        
        for stat in user_stats:
            role_stats[stat.role.value] = {
                'total': stat.count,
                'active': stat.active_count
            }
            total_users += stat.count
            total_active += stat.active_count
        
        return {
            'total': total_users,
            'active': total_active,
            'by_role': role_stats
        }

class BusinessService:
    """Service class for business management operations"""
    
    @staticmethod
    def create_business(db: Session, owner_id: str, business_data: BusinessCreate) -> Business:
        """Create a new business"""
        
        # Check if user already has a business
        existing_business = db.query(Business).filter(Business.owner_id == owner_id).first()
        if existing_business:
            raise ValueError("User already has a registered business")
        
        # Create new business
        new_business = Business(
            owner_id=owner_id,
            business_name=business_data.business_name,
            business_type=business_data.business_type,
            address=business_data.address,
            phone=business_data.phone,
            registration_number=business_data.registration_number,
            is_verified=False
        )
        
        db.add(new_business)
        db.commit()
        db.refresh(new_business)
        
        logger.info(f"Business created: {new_business.business_name}")
        return new_business
    
    @staticmethod
    def get_business_by_id(db: Session, business_id: str) -> Optional[Business]:
        """Get business by ID"""
        return db.query(Business).options(joinedload(Business.owner)).filter(
            Business.id == business_id
        ).first()
    
    @staticmethod
    def get_business_by_owner(db: Session, owner_id: str) -> Optional[Business]:
        """Get business by owner ID"""
        return db.query(Business).options(joinedload(Business.owner)).filter(
            Business.owner_id == owner_id
        ).first()
    
    @staticmethod
    def get_businesses_paginated(
        db: Session,
        page: int = 1,
        size: int = 10,
        is_verified: Optional[bool] = None,
        search: Optional[str] = None,
        owner_id: Optional[str] = None
    ) -> Tuple[List[Business], int]:
        """Get paginated list of businesses with filters"""
        
        query = db.query(Business).options(joinedload(Business.owner))
        
        # Apply filters
        if is_verified is not None:
            query = query.filter(Business.is_verified == is_verified)
        
        if search:
            search_filter = or_(
                Business.business_name.ilike(f"%{search}%"),
                Business.business_type.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if owner_id:
            query = query.filter(Business.owner_id == owner_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        businesses = query.offset(offset).limit(size).all()
        
        return businesses, total
    
    @staticmethod
    def update_business(db: Session, business_id: str, update_data: Dict[str, Any]) -> Optional[Business]:
        """Update business information"""
        
        business = db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return None
        
        # Update business fields
        for field, value in update_data.items():
            if hasattr(business, field):
                setattr(business, field, value)
        
        db.commit()
        db.refresh(business)
        
        logger.info(f"Business updated: {business.business_name}")
        return business
    
    @staticmethod
    def verify_business(db: Session, business_id: str) -> bool:
        """Verify business"""
        
        business = db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return False
        
        business.is_verified = True
        db.commit()
        
        logger.info(f"Business verified: {business.business_name}")
        return True
    
    @staticmethod
    def unverify_business(db: Session, business_id: str) -> bool:
        """Unverify business"""
        
        business = db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return False
        
        business.is_verified = False
        db.commit()
        
        logger.info(f"Business unverified: {business.business_name}")
        return True
    
    @staticmethod
    def get_business_statistics(db: Session) -> Dict[str, Any]:
        """Get business statistics"""
        
        business_stats = db.query(
            func.count(Business.id).label('total_businesses'),
            func.count(func.nullif(Business.is_verified, False)).label('verified_businesses')
        ).first()
        
        return {
            'total': business_stats.total_businesses,
            'verified': business_stats.verified_businesses
        }