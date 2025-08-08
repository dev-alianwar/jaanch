"""
Business request approval routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
import logging
from datetime import datetime, date
from decimal import Decimal

from database import get_db
from auth import get_current_business, get_current_superadmin, get_current_user
from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    RequestStatus, PlanStatus, PaymentStatus, UserRole
)
from schemas import (
    InstallmentRequestResponse, RequestApproval, RequestRejection,
    InstallmentPlanResponse, CustomerInstallmentHistory, PaginatedResponse
)
from approval_service import ApprovalService, PaymentService
from fraud_service import FraudDetectionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/approvals", tags=["Request Approval"])

@router.post("/requests/{request_id}/approve", response_model=InstallmentPlanResponse)
async def approve_installment_request(
    request_id: str,
    approval_data: RequestApproval,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Approve installment request and create installment plan"""
    
    # Get the installment request
    request_obj = db.query(InstallmentRequest).options(
        joinedload(InstallmentRequest.customer),
        joinedload(InstallmentRequest.business)
    ).filter(InstallmentRequest.id == request_id).first()
    
    if not request_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installment request not found"
        )
    
    # Verify business ownership
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business or request_obj.business_id != user_business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to approve this request"
        )
    
    # Check if request is still pending
    if request_obj.status != RequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request is not in pending status"
        )
    
    try:
        # Use approval service to handle the approval process
        installment_plan = ApprovalService.approve_request(
            db=db,
            request_id=request_id,
            business_notes=approval_data.business_notes
        )
        
        logger.info(f"Request approved: {request_id} by business {current_user.email}")
        
        return InstallmentPlanResponse.from_orm(installment_plan)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error approving request {request_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve request"
        )

@router.post("/requests/{request_id}/reject")
async def reject_installment_request(
    request_id: str,
    rejection_data: RequestRejection,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Reject installment request"""
    
    # Get the installment request
    request_obj = db.query(InstallmentRequest).filter(
        InstallmentRequest.id == request_id
    ).first()
    
    if not request_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installment request not found"
        )
    
    # Verify business ownership
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business or request_obj.business_id != user_business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reject this request"
        )
    
    # Check if request is still pending
    if request_obj.status != RequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request is not in pending status"
        )
    
    try:
        # Use approval service to handle the rejection
        ApprovalService.reject_request(
            db=db,
            request_id=request_id,
            business_notes=rejection_data.business_notes
        )
        
        logger.info(f"Request rejected: {request_id} by business {current_user.email}")
        
        return {"message": "Request rejected successfully"}
        
    except Exception as e:
        logger.error(f"Error rejecting request {request_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reject request"
        )

@router.get("/customer-history/{customer_id}", response_model=CustomerInstallmentHistory)
async def get_customer_installment_history(
    customer_id: str,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get complete installment history for a customer (for business decision making)"""
    
    # Verify the customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    try:
        # Get comprehensive customer history using fraud detection service
        history = FraudDetectionService.get_customer_complete_history(db, customer_id)
        
        logger.info(f"Customer history accessed: {customer_id} by business {current_user.email}")
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting customer history {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve customer history"
        )

@router.get("/pending-requests", response_model=PaginatedResponse)
async def get_pending_requests_for_business(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(created_at|product_value|installment_months)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get pending installment requests for current business with customer history"""
    
    # Get user's business
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business found for current user"
        )
    
    try:
        # Get pending requests with enhanced information
        requests, total = ApprovalService.get_pending_requests_with_history(
            db=db,
            business_id=str(user_business.id),
            page=page,
            size=size,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Calculate total pages
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=requests,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Error getting pending requests for business {user_business.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pending requests"
        )

@router.get("/installment-plans", response_model=PaginatedResponse)
async def get_business_installment_plans(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status_filter: Optional[PlanStatus] = None,
    customer_search: Optional[str] = None,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get installment plans for current business"""
    
    # Get user's business
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business found for current user"
        )
    
    query = db.query(InstallmentPlan).options(
        joinedload(InstallmentPlan.customer),
        joinedload(InstallmentPlan.business)
    ).filter(InstallmentPlan.business_id == user_business.id)
    
    # Apply filters
    if status_filter:
        query = query.filter(InstallmentPlan.status == status_filter)
    
    if customer_search:
        query = query.join(User).filter(
            or_(
                User.first_name.ilike(f"%{customer_search}%"),
                User.last_name.ilike(f"%{customer_search}%"),
                User.email.ilike(f"%{customer_search}%")
            )
        )
    
    # Order by creation date (newest first)
    query = query.order_by(desc(InstallmentPlan.created_at))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    plans = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[InstallmentPlanResponse.from_orm(plan) for plan in plans],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/installment-plans/{plan_id}", response_model=InstallmentPlanResponse)
async def get_installment_plan_details(
    plan_id: str,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get detailed installment plan information"""
    
    plan = db.query(InstallmentPlan).options(
        joinedload(InstallmentPlan.customer),
        joinedload(InstallmentPlan.business),
        joinedload(InstallmentPlan.payments)
    ).filter(InstallmentPlan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installment plan not found"
        )
    
    # Verify business ownership
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business or plan.business_id != user_business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this installment plan"
        )
    
    return InstallmentPlanResponse.from_orm(plan)

@router.post("/installment-plans/{plan_id}/record-payment")
async def record_payment(
    plan_id: str,
    payment_amount: Decimal,
    payment_method: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Record a payment for an installment plan"""
    
    # Get the installment plan
    plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installment plan not found"
        )
    
    # Verify business ownership
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business or plan.business_id != user_business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to record payment for this plan"
        )
    
    try:
        # Use payment service to record the payment
        payment = PaymentService.record_payment(
            db=db,
            plan_id=plan_id,
            amount=payment_amount,
            payment_method=payment_method,
            notes=notes
        )
        
        logger.info(f"Payment recorded: {payment.id} for plan {plan_id} by business {current_user.email}")
        
        return {
            "message": "Payment recorded successfully",
            "payment_id": str(payment.id),
            "remaining_amount": float(plan.remaining_amount)
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error recording payment for plan {plan_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record payment"
        )

@router.get("/business-analytics")
async def get_business_analytics(
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get analytics and statistics for current business"""
    
    # Get user's business
    user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
    if not user_business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business found for current user"
        )
    
    try:
        analytics = ApprovalService.get_business_analytics(db, str(user_business.id))
        return analytics
        
    except Exception as e:
        logger.error(f"Error getting business analytics for {user_business.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve business analytics"
        )

@router.get("/risk-assessment/{customer_id}")
async def get_customer_risk_assessment(
    customer_id: str,
    current_user: User = Depends(get_current_business),
    db: Session = Depends(get_db)
):
    """Get risk assessment for a customer"""
    
    # Verify the customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    try:
        # Get risk assessment using fraud detection service
        risk_assessment = FraudDetectionService.calculate_customer_risk_score(db, customer_id)
        
        logger.info(f"Risk assessment accessed: {customer_id} by business {current_user.email}")
        
        return risk_assessment
        
    except Exception as e:
        logger.error(f"Error getting risk assessment for customer {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve risk assessment"
        )