"""
Installment request service layer
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from database.models import (
    User, Business, InstallmentRequest, RequestStatus, 
    UserRole, FraudAlert, AlertType, AlertSeverity
)
from app.schemas.installment import InstallmentRequestCreate

logger = logging.getLogger(__name__)

class InstallmentRequestService:
    """Service class for installment request operations"""
    
    @staticmethod
    def create_request(
        db: Session, 
        customer_id: str, 
        request_data: InstallmentRequestCreate
    ) -> InstallmentRequest:
        """Create a new installment request with validation"""
        
        # Verify business exists and is verified
        business = db.query(Business).filter(
            Business.id == request_data.business_id,
            Business.is_verified == True
        ).first()
        
        if not business:
            raise ValueError("Business not found or not verified")
        
        # Validate product value and installment terms
        if request_data.product_value <= 0:
            raise ValueError("Product value must be greater than 0")
        
        if request_data.installment_months < 1 or request_data.installment_months > 60:
            raise ValueError("Installment months must be between 1 and 60")
        
        # Calculate monthly amount
        monthly_amount = request_data.product_value / request_data.installment_months
        
        # Check for duplicate pending requests
        existing_request = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.business_id == request_data.business_id,
            InstallmentRequest.status == RequestStatus.PENDING,
            InstallmentRequest.product_name == request_data.product_name
        ).first()
        
        if existing_request:
            raise ValueError("Duplicate pending request exists for this product")
        
        # Check for rapid request pattern (fraud detection)
        recent_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        if recent_requests >= 5:  # More than 5 requests in 24 hours
            InstallmentRequestService._create_fraud_alert(
                db, customer_id, AlertType.RAPID_REQUESTS,
                f"Customer made {recent_requests + 1} requests in 24 hours",
                {"request_count": recent_requests + 1, "timeframe": "24_hours"}
            )
        
        # Create new installment request
        new_request = InstallmentRequest(
            customer_id=customer_id,
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
        
        logger.info(f"Installment request created: {new_request.id}")
        return new_request
    
    @staticmethod
    def get_request_by_id(db: Session, request_id: str) -> Optional[InstallmentRequest]:
        """Get installment request by ID with relationships"""
        return db.query(InstallmentRequest).options(
            joinedload(InstallmentRequest.customer),
            joinedload(InstallmentRequest.business).joinedload(Business.owner)
        ).filter(InstallmentRequest.id == request_id).first()
    
    @staticmethod
    def get_requests_paginated(
        db: Session,
        page: int = 1,
        size: int = 10,
        customer_id: Optional[str] = None,
        business_id: Optional[str] = None,
        status_filter: Optional[RequestStatus] = None
    ) -> Tuple[List[InstallmentRequest], int]:
        """Get paginated installment requests with filters"""
        
        query = db.query(InstallmentRequest).options(
            joinedload(InstallmentRequest.customer),
            joinedload(InstallmentRequest.business).joinedload(Business.owner)
        )
        
        # Apply filters
        if customer_id:
            query = query.filter(InstallmentRequest.customer_id == customer_id)
        
        if business_id:
            query = query.filter(InstallmentRequest.business_id == business_id)
        
        if status_filter:
            query = query.filter(InstallmentRequest.status == status_filter)
        
        # Order by creation date (newest first)
        query = query.order_by(desc(InstallmentRequest.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        requests = query.offset(offset).limit(size).all()
        
        return requests, total
    
    @staticmethod
    def check_customer_eligibility(db: Session, customer_id: str, business_id: str) -> Dict[str, Any]:
        """Check customer eligibility for new installment request"""
        
        # Get customer's active requests count
        active_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.status.in_([RequestStatus.PENDING, RequestStatus.APPROVED])
        ).count()
        
        # Get recent request count (last 24 hours)
        recent_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        # Get total debt amount (from approved requests)
        total_debt = db.query(func.coalesce(func.sum(InstallmentRequest.product_value), 0)).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.status == RequestStatus.APPROVED
        ).scalar()
        
        # Check for existing pending request with same business
        existing_pending = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.business_id == business_id,
            InstallmentRequest.status == RequestStatus.PENDING
        ).first()
        
        # Determine eligibility
        max_active_requests = 5  # Configurable limit
        max_recent_requests = 3  # Max requests in 24 hours
        max_debt_amount = Decimal('50000')  # Configurable limit
        
        is_eligible = (
            active_requests < max_active_requests and
            recent_requests < max_recent_requests and
            total_debt < max_debt_amount and
            not existing_pending
        )
        
        return {
            "eligible": is_eligible,
            "active_requests": active_requests,
            "recent_requests": recent_requests,
            "total_debt": float(total_debt),
            "has_pending_with_business": existing_pending is not None,
            "limits": {
                "max_active_requests": max_active_requests,
                "max_recent_requests": max_recent_requests,
                "max_debt_amount": float(max_debt_amount)
            }
        }
    
    @staticmethod
    def _create_fraud_alert(
        db: Session,
        customer_id: str,
        alert_type: AlertType,
        description: str,
        metadata: Dict[str, Any]
    ):
        """Create a fraud alert for suspicious activity"""
        
        # Check if similar alert already exists
        existing_alert = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id,
            FraudAlert.alert_type == alert_type,
            FraudAlert.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).first()
        
        if existing_alert:
            return  # Don't create duplicate alerts
        
        # Determine severity based on alert type
        severity = AlertSeverity.MEDIUM
        if alert_type == AlertType.RAPID_REQUESTS:
            if metadata.get('request_count', 0) > 10:
                severity = AlertSeverity.HIGH
        
        fraud_alert = FraudAlert(
            customer_id=customer_id,
            alert_type=alert_type,
            description=description,
            alert_metadata=metadata,
            severity=severity
        )
        
        db.add(fraud_alert)
        db.commit()
        
        logger.warning(f"Fraud alert created: {alert_type} for customer {customer_id}")


class BusinessService:
    """Service class for business-related installment operations"""
    
    @staticmethod
    def get_verified_businesses(db: Session) -> List[Business]:
        """Get all verified businesses available for installment requests"""
        return db.query(Business).options(joinedload(Business.owner)).filter(
            Business.is_verified == True
        ).all()
    
    @staticmethod
    def get_business_by_owner(db: Session, owner_id: str) -> Optional[Business]:
        """Get business by owner ID"""
        return db.query(Business).filter(Business.owner_id == owner_id).first()