"""
Customer installment history routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from database import get_db
from auth import get_current_user, get_current_business, get_current_superadmin
from models import User, Business, InstallmentPlan, UserRole
from schemas import (
    CustomerInstallmentHistory, InstallmentPlanResponse, 
    PaginatedResponse, UserResponse
)
from history_service import HistoryService
from fraud_service import FraudDetectionService

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
            items=[InstallmentPlanResponse.from_orm(plan) for plan in plans],
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

@router.get("/payment-history", response_model=PaginatedResponse)
async def get_payment_history(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    plan_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payment history for current customer"""
    
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access personal payment history"
        )
    
    try:
        # Parse date filters if provided
        date_from_parsed = None
        date_to_parsed = None
        
        if date_from:
            try:
                date_from_parsed = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date_from format. Use ISO format."
                )
        
        if date_to:
            try:
                date_to_parsed = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date_to format. Use ISO format."
                )
        
        payments, total = HistoryService.get_customer_payment_history(
            db=db,
            customer_id=str(current_user.id),
            page=page,
            size=size,
            plan_id=plan_id,
            date_from=date_from_parsed,
            date_to=date_to_parsed
        )
        
        # Calculate total pages
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=payments,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting payment history for {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve payment history"
        )

@router.get("/business-relationships")
async def get_business_relationships(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all businesses the customer has had installment relationships with"""
    
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access business relationships"
        )
    
    try:
        relationships = HistoryService.get_customer_business_relationships(
            db, str(current_user.id)
        )
        
        return {
            "customer_id": str(current_user.id),
            "total_businesses": len(relationships),
            "relationships": relationships
        }
        
    except Exception as e:
        logger.error(f"Error getting business relationships for {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve business relationships"
        )

@router.get("/statistics")
async def get_customer_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive statistics for current customer"""
    
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can access personal statistics"
        )
    
    try:
        stats = HistoryService.get_customer_statistics(db, str(current_user.id))
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting statistics for {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer statistics"
        )

@router.get("/cross-business-analysis/{customer_id}")
async def get_cross_business_analysis(
    customer_id: str,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get cross-business analysis for a customer (business users only)"""
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get user's business
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business found for current user"
        )
    
    # Check if customer has interaction with this business
    has_interaction = HistoryService.customer_has_business_interaction(
        db, customer_id, str(user_business.id)
    )
    if not has_interaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No business relationship with this customer"
        )
    
    try:
        analysis = HistoryService.get_cross_business_analysis(db, customer_id)
        
        logger.info(f"Cross-business analysis accessed: {customer_id} by business {current_user.email}")
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error getting cross-business analysis for {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cross-business analysis"
        )

@router.get("/fraud-indicators/{customer_id}")
async def get_customer_fraud_indicators(
    customer_id: str,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get fraud indicators for a customer (business users only)"""
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Get user's business
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business found for current user"
        )
    
    # Check if customer has interaction with this business
    has_interaction = HistoryService.customer_has_business_interaction(
        db, customer_id, str(user_business.id)
    )
    if not has_interaction:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No business relationship with this customer"
        )
    
    try:
        # Get fraud indicators using fraud detection service
        fraud_indicators = FraudDetectionService.calculate_customer_risk_score(db, customer_id)
        
        logger.info(f"Fraud indicators accessed: {customer_id} by business {current_user.email}")
        
        return fraud_indicators
        
    except Exception as e:
        logger.error(f"Error getting fraud indicators for {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve fraud indicators"
        )

@router.get("/timeline/{customer_id}")
async def get_customer_timeline(
    customer_id: str,
    days: int = Query(90, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get customer installment timeline (chronological activity)"""
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER:
        if str(current_user.id) != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this customer's timeline"
            )
    elif current_user.role == UserRole.BUSINESS:
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No business found for current user"
            )
        
        has_interaction = HistoryService.customer_has_business_interaction(
            db, customer_id, str(user_business.id)
        )
        if not has_interaction:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No business relationship with this customer"
            )
    # Superadmins can view any timeline
    
    try:
        timeline = HistoryService.get_customer_timeline(db, customer_id, days)
        
        logger.info(f"Customer timeline accessed: {customer_id} by {current_user.role} {current_user.email}")
        
        return {
            "customer_id": customer_id,
            "timeline_days": days,
            "events": timeline
        }
        
    except Exception as e:
        logger.error(f"Error getting timeline for {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer timeline"
        )