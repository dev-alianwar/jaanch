"""
Customer installment history routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from database import get_db, User, UserRole, Business, InstallmentPlan
from app.api.dependencies import get_current_user, get_current_business, get_current_superadmin
from app.schemas.history import (
    CustomerInstallmentHistory, InstallmentPlanResponse, 
    PaginatedResponse, UserResponse
)
from .history_service import HistoryService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["Customer History"])

@router.get("/customer/{customer_id}", response_model=CustomerInstallmentHistory)
async def get_customer_installment_history(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete installment history for a customer (cross-business visibility)"""
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER:
        # Customers can only view their own history
        if str(current_user.id) != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this customer's history"
            )
    elif current_user.role == UserRole.BUSINESS:
        # Business users can view history for customers who have requests with them
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No business found for current user"
            )
        
        # Check if customer has any interaction with this business
        has_interaction = HistoryService.customer_has_business_interaction(
            db, customer_id, str(user_business.id)
        )
        if not has_interaction:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No business relationship with this customer"
            )
    # Superadmins can view any customer's history
    
    try:
        # Get comprehensive customer history
        history = HistoryService.get_complete_customer_history(db, customer_id)
        
        logger.info(f"Customer history accessed: {customer_id} by {current_user.role} {current_user.email}")
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting customer history {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer history"
        )

@router.get("/my-history", response_model=CustomerInstallmentHistory)
async def get_my_installment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's complete installment history"""
    
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access personal history"
        )
    
    try:
        history = HistoryService.get_complete_customer_history(db, str(current_user.id))
        
        logger.info(f"Personal history accessed by customer {current_user.email}")
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting personal history for {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve personal history"
        )

@router.get("/active-plans", response_model=PaginatedResponse)
async def get_active_installment_plans(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    business_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active installment plans for current customer"""
    
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access personal active plans"
        )
    
    try:
        plans, total = HistoryService.get_customer_active_plans(
            db=db,
            customer_id=str(current_user.id),
            page=page,
            size=size,
            business_filter=business_filter
        )
        
        # Calculate total pages
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=[InstallmentPlanResponse.model_validate(plan) for plan in plans],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Error getting active plans for {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve active plans"
        )