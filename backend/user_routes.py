"""
User management routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
import logging
from datetime import datetime

from database import get_db
from auth import (
    get_current_user, get_current_superadmin, get_current_business,
    rate_limit
)
from models import User, Business, UserRole
from schemas import (
    UserResponse, UserRegister, BusinessResponse, BusinessCreate, 
    BusinessUpdate, PaginationParams, PaginatedResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/", response_model=PaginatedResponse)
async def get_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    role: Optional[UserRole] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get paginated list of users (superadmin only)"""
    
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
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[UserResponse.from_orm(user) for user in users],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user by ID"""
    
    # Users can only view their own profile unless they're superadmin
    if current_user.role != UserRole.SUPERADMIN and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user information"""
    
    # Users can only update their own profile unless they're superadmin
    if current_user.role != UserRole.SUPERADMIN and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'phone']
    if current_user.role == UserRole.SUPERADMIN:
        allowed_fields.extend(['is_active', 'role'])
    
    for field, value in user_update.items():
        if field in allowed_fields and hasattr(user, field):
            setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    logger.info(f"User updated: {user.email} by {current_user.email}")
    
    return UserResponse.from_orm(user)

@router.delete("/{user_id}")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Deactivate user (superadmin only)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deactivating superadmin users
    if user.role == UserRole.SUPERADMIN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate superadmin users"
        )
    
    user.is_active = False
    user.updated_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"User deactivated: {user.email} by {current_user.email}")
    
    return {"message": "User deactivated successfully"}

@router.post("/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Activate user (superadmin only)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    user.updated_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"User activated: {user.email} by {current_user.email}")
    
    return {"message": "User activated successfully"}

# Business management endpoints
@router.get("/businesses/", response_model=PaginatedResponse)
async def get_businesses(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    is_verified: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of businesses"""
    
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
    
    # Business users can only see their own business
    if current_user.role == UserRole.BUSINESS:
        query = query.filter(Business.owner_id == current_user.id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    businesses = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[BusinessResponse.from_orm(business) for business in businesses],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/businesses/{business_id}", response_model=BusinessResponse)
async def get_business_by_id(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get business by ID"""
    
    business = db.query(Business).options(joinedload(Business.owner)).filter(
        Business.id == business_id
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Business users can only view their own business
    if (current_user.role == UserRole.BUSINESS and 
        business.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this business"
        )
    
    return BusinessResponse.from_orm(business)

@router.put("/businesses/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: str,
    business_update: BusinessUpdate,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Update business information"""
    
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Business users can only update their own business
    if (current_user.role == UserRole.BUSINESS and 
        business.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this business"
        )
    
    # Update business fields
    update_data = business_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(business, field):
            setattr(business, field, value)
    
    db.commit()
    db.refresh(business)
    
    logger.info(f"Business updated: {business.business_name} by {current_user.email}")
    
    return BusinessResponse.from_orm(business)

@router.post("/businesses/{business_id}/verify")
async def verify_business(
    business_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Verify business (superadmin only)"""
    
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    business.is_verified = True
    db.commit()
    
    logger.info(f"Business verified: {business.business_name} by {current_user.email}")
    
    return {"message": "Business verified successfully"}

@router.post("/businesses/{business_id}/unverify")
async def unverify_business(
    business_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Unverify business (superadmin only)"""
    
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    business.is_verified = False
    db.commit()
    
    logger.info(f"Business unverified: {business.business_name} by {current_user.email}")
    
    return {"message": "Business unverified successfully"}

@router.get("/stats/overview")
async def get_user_stats(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get user statistics overview (superadmin only)"""
    
    # Get user counts by role
    user_stats = db.query(
        User.role,
        func.count(User.id).label('count'),
        func.count(func.nullif(User.is_active, False)).label('active_count')
    ).group_by(User.role).all()
    
    # Get business stats
    business_stats = db.query(
        func.count(Business.id).label('total_businesses'),
        func.count(func.nullif(Business.is_verified, False)).label('verified_businesses')
    ).first()
    
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
        'users': {
            'total': total_users,
            'active': total_active,
            'by_role': role_stats
        },
        'businesses': {
            'total': business_stats.total_businesses,
            'verified': business_stats.verified_businesses
        }
    }

@router.get("/profile", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile"""
    return UserResponse.from_orm(current_user)

@router.put("/profile", response_model=UserResponse)
async def update_current_user_profile(
    profile_update: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    
    # Only allow updating certain fields
    allowed_fields = ['first_name', 'last_name', 'phone']
    
    for field, value in profile_update.items():
        if field in allowed_fields and hasattr(current_user, field):
            setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"Profile updated: {current_user.email}")
    
    return UserResponse.from_orm(current_user)