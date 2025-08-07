"""
Authentication routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
import logging

from database import get_db
from auth import (
    AuthService, authenticate_user, get_current_user, 
    RateLimiter, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
)
from models import User, Business, UserRole
from schemas import (
    UserLogin, UserRegister, UserResponse, AuthResponse, 
    TokenRefresh, PasswordChange, BusinessCreate, BusinessResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    request: Request,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    
    # Rate limiting for registration
    client_ip = request.client.host
    rate_limit_key = f"register:{client_ip}"
    if RateLimiter.is_rate_limited(rate_limit_key, limit=5, window=300):  # 5 registrations per 5 minutes
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Please try again later."
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
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
    
    # Create tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role.value},
        expires_delta=access_token_expires
    )
    refresh_token = AuthService.create_refresh_token(
        data={"sub": str(new_user.id), "email": new_user.email}
    )
    
    # Store session
    AuthService.store_session(
        str(new_user.id), 
        access_token, 
        ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    logger.info(f"New user registered: {new_user.email} with role {new_user.role}")
    
    return AuthResponse(
        user=UserResponse.from_orm(new_user),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/login", response_model=AuthResponse)
async def login_user(
    user_credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Login user and return JWT tokens"""
    
    # Rate limiting for login attempts
    client_ip = request.client.host
    rate_limit_key = f"login:{client_ip}"
    if RateLimiter.is_rate_limited(rate_limit_key, limit=10, window=300):  # 10 attempts per 5 minutes
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    # Authenticate user
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        # Increment failed login attempts
        failed_key = f"failed_login:{user_credentials.email}"
        RateLimiter.is_rate_limited(failed_key, limit=5, window=900)  # Track failed attempts
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    refresh_token = AuthService.create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # Store session
    AuthService.store_session(
        str(user.id), 
        access_token, 
        ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return AuthResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    payload = AuthService.verify_token(token_data.refresh_token)
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    new_refresh_token = AuthService.create_refresh_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # Update session
    AuthService.store_session(
        str(user.id), 
        access_token, 
        ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    return AuthResponse(
        user=UserResponse.from_orm(user),
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user)):
    """Logout user and invalidate session"""
    
    # Invalidate session
    AuthService.invalidate_session(str(current_user.id))
    
    logger.info(f"User logged out: {current_user.email}")
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)

@router.put("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    
    # Verify current password
    if not AuthService.verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    new_password_hash = AuthService.get_password_hash(password_data.new_password)
    current_user.password_hash = new_password_hash
    
    db.commit()
    
    # Invalidate all sessions to force re-login
    AuthService.invalidate_session(str(current_user.id))
    
    logger.info(f"Password changed for user: {current_user.email}")
    
    return {"message": "Password changed successfully. Please login again."}

@router.post("/business/register", response_model=BusinessResponse)
async def register_business(
    business_data: BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register a new business (for business users)"""
    
    # Only business users can register businesses
    if current_user.role != UserRole.BUSINESS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only business users can register businesses"
        )
    
    # Check if user already has a business
    existing_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if existing_business:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a registered business"
        )
    
    # Create new business
    new_business = Business(
        owner_id=current_user.id,
        business_name=business_data.business_name,
        business_type=business_data.business_type,
        address=business_data.address,
        phone=business_data.phone,
        registration_number=business_data.registration_number,
        is_verified=False  # Requires admin verification
    )
    
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    
    logger.info(f"New business registered: {new_business.business_name} by {current_user.email}")
    
    return BusinessResponse.from_orm(new_business)

@router.get("/session/info")
async def get_session_info(current_user: User = Depends(get_current_user)):
    """Get current session information"""
    
    session = AuthService.get_session(str(current_user.id))
    rate_limit_info = RateLimiter.get_rate_limit_info(f"rate_limit:{current_user.id}")
    
    return {
        "user_id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role,
        "session_active": session is not None,
        "rate_limit": rate_limit_info
    }