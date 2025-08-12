"""
Installment request management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
import logging
from datetime import datetime
from decimal import Decimal

from app.core.database import get_db
from app.api.dependencies import (
    get_current_user, get_current_customer, get_current_business,
    get_current_superadmin
)
from app.models.user import User, UserRole
from database.models import Business, InstallmentRequest, RequestStatus
from app.schemas.installment import (
    InstallmentRequestCreate, InstallmentRequestUpdate, InstallmentRequestResponse,
    RequestApproval, RequestRejection, PaginatedResponse, BusinessResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/installments", tags=["Installment Requests"])

@router.get("/businesses", response_model=List[BusinessResponse])
async def get_available_businesses(
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Get list of verified businesses available for installment requests"""
    
    businesses = db.query(Business).options(joinedload(Business.owner)).filter(
        Business.is_verified == True
    ).all()
    
    return [BusinessResponse.model_validate(business) for business in businesses]

@router.post("/requests", response_model=InstallmentRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_installment_request(
    request_data: InstallmentRequestCreate,
    current_user: User = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """Create a new installment request (customers only)"""
    
    # Verify business exists and is verified
    business = db.query(Business).filter(
        Business.id == request_data.business_id,
        Business.is_verified == True
    ).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found or not verified"
        )
    
    # Validate product value and installment terms
    if request_data.product_value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product value must be greater than 0"
        )
    
    if request_data.installment_months < 1 or request_data.installment_months > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Installment months must be between 1 and 60"
        )
    
    # Calculate monthly amount
    monthly_amount = request_data.product_value / request_data.installment_months
    
    # Check for duplicate pending requests
    existing_request = db.query(InstallmentRequest).filter(
        InstallmentRequest.customer_id == current_user.id,
        InstallmentRequest.business_id == request_data.business_id,
        InstallmentRequest.status == RequestStatus.PENDING,
        InstallmentRequest.product_name == request_data.product_name
    ).first()
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have a pending request for this product with this business"
        )
    
    # Create new installment request
    new_request = InstallmentRequest(
        customer_id=current_user.id,
        business_id=request_data.business_id,
        product_name=request_data.product_name,
        product_description=request_data.product_description,
        product_value=request_data.product_value,
        installment_months=request_data.installment_months,
        monthly_amount=monthly_amount,
        status=RequestStatus.PENDING
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    # Load relationships for response
    request_with_relations = db.query(InstallmentRequest).options(
        joinedload(InstallmentRequest.customer),
        joinedload(InstallmentRequest.business).joinedload(Business.owner)
    ).filter(InstallmentRequest.id == new_request.id).first()
    
    logger.info(f"Installment request created: {new_request.id} by customer {current_user.email}")
    
    return InstallmentRequestResponse.model_validate(request_with_relations)

@router.get("/requests", response_model=PaginatedResponse)
async def get_installment_requests(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status_filter: Optional[RequestStatus] = None,
    business_id: Optional[str] = None,
    customer_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of installment requests"""
    
    query = db.query(InstallmentRequest).options(
        joinedload(InstallmentRequest.customer),
        joinedload(InstallmentRequest.business).joinedload(Business.owner)
    )
    
    # Apply role-based filtering
    if current_user.role == UserRole.CUSTOMER:
        # Customers can only see their own requests
        query = query.filter(InstallmentRequest.customer_id == current_user.id)
    elif current_user.role == UserRole.BUSINESS:
        # Business users can only see requests for their business
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No business found for current user"
            )
        query = query.filter(InstallmentRequest.business_id == user_business.id)
    # Superadmins can see all requests (no additional filtering)
    
    # Apply additional filters
    if status_filter:
        query = query.filter(InstallmentRequest.status == status_filter)
    
    if business_id and current_user.role == UserRole.SUPERADMIN:
        query = query.filter(InstallmentRequest.business_id == business_id)
    
    if customer_id and current_user.role in [UserRole.SUPERADMIN, UserRole.BUSINESS]:
        query = query.filter(InstallmentRequest.customer_id == customer_id)
    
    # Order by creation date (newest first)
    query = query.order_by(desc(InstallmentRequest.created_at))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    requests = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[InstallmentRequestResponse.model_validate(req) for req in requests],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/requests/{request_id}", response_model=InstallmentRequestResponse)
async def get_installment_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get installment request by ID"""
    
    request_obj = db.query(InstallmentRequest).options(
        joinedload(InstallmentRequest.customer),
        joinedload(InstallmentRequest.business).joinedload(Business.owner)
    ).filter(InstallmentRequest.id == request_id).first()
    
    if not request_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Installment request not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER:
        if request_obj.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this request"
            )
    elif current_user.role == UserRole.BUSINESS:
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business or request_obj.business_id != user_business.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this request"
            )
    # Superadmins can view any request
    
    return InstallmentRequestResponse.model_validate(request_obj)