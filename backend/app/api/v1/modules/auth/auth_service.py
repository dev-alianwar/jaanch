"""
Authentication service with business logic
"""
from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import SecurityService
from app.core.config import settings
from app.core.logging import get_logger
from app.models.user import User, UserRole
from app.schemas.auth import UserRegister, UserLogin, AuthResponse, UserResponse

logger = get_logger("auth_service")


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> AuthResponse:
        """Register a new user"""
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = SecurityService.get_password_hash(user_data.password)
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
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        access_token = SecurityService.create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role.value},
            expires_delta=access_token_expires
        )
        refresh_token = SecurityService.create_refresh_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )
        
        logger.info(f"New user registered: {new_user.email} with role {new_user.role}")
        
        return AuthResponse(
            user=UserResponse.model_validate(new_user),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email, User.is_active == True).first()
        if not user:
            return None
        
        if not SecurityService.verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> AuthResponse:
        """Login user and return JWT tokens"""
        
        # Authenticate user
        user = AuthService.authenticate_user(db, login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create tokens
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        access_token = SecurityService.create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value},
            expires_delta=access_token_expires
        )
        refresh_token = SecurityService.create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        logger.info(f"User logged in: {user.email}")
        
        return AuthResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> AuthResponse:
        """Refresh access token using refresh token"""
        
        # Verify refresh token
        payload = SecurityService.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        access_token = SecurityService.create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value},
            expires_delta=access_token_expires
        )
        new_refresh_token = SecurityService.create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return AuthResponse(
            user=UserResponse.model_validate(user),
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.JWT_EXPIRE_MINUTES * 60
        )