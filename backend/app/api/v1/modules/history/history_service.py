"""
Customer history service layer
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from database.models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, RequestStatus, PlanStatus, PaymentStatus
)
from app.schemas.history import (
    CustomerInstallmentHistory, UserResponse, InstallmentPlanResponse,
    FraudAlertResponse, FraudPatternResponse, PaymentResponse
)

logger = logging.getLogger(__name__)

class HistoryService:
    """Service class for customer installment history operations"""
    
    @staticmethod
    def get_complete_customer_history(db: Session, customer_id: str) -> CustomerInstallmentHistory:
        """Get complete installment history for a customer across all businesses"""
        
        # Get customer
        customer = db.query(User).filter(User.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        # Get active installment plans
        active_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).order_by(desc(InstallmentPlan.created_at)).all()
        
        # Get completed installment plans
        completed_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.COMPLETED
        ).order_by(desc(InstallmentPlan.created_at)).all()
        
        # Get fraud alerts
        fraud_alerts = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id
        ).order_by(desc(FraudAlert.created_at)).all()
        
        # Get fraud patterns
        fraud_patterns = db.query(FraudPattern).filter(
            FraudPattern.customer_id == customer_id
        ).order_by(desc(FraudPattern.detected_at)).all()
        
        # Calculate totals
        total_active_debt = sum(plan.remaining_amount for plan in active_plans)
        total_completed_amount = sum(plan.total_amount for plan in completed_plans)
        
        # Calculate risk score (simplified version)
        risk_score = HistoryService._calculate_simple_risk_score(
            active_plans, completed_plans, fraud_alerts
        )
        
        return CustomerInstallmentHistory(
            customer=UserResponse.model_validate(customer),
            active_plans=[InstallmentPlanResponse.model_validate(plan) for plan in active_plans],
            completed_plans=[InstallmentPlanResponse.model_validate(plan) for plan in completed_plans],
            total_active_debt=total_active_debt,
            total_completed_amount=total_completed_amount,
            fraud_alerts=[FraudAlertResponse.model_validate(alert) for alert in fraud_alerts],
            fraud_patterns=[FraudPatternResponse.model_validate(pattern) for pattern in fraud_patterns],
            risk_score=Decimal(str(risk_score))
        )
    
    @staticmethod
    def get_customer_active_plans(
        db: Session,
        customer_id: str,
        page: int = 1,
        size: int = 10,
        business_filter: Optional[str] = None
    ) -> Tuple[List[InstallmentPlan], int]:
        """Get paginated active installment plans for a customer"""
        
        query = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        )
        
        # Apply business filter if provided
        if business_filter:
            query = query.join(Business).filter(
                Business.business_name.ilike(f"%{business_filter}%")
            )
        
        # Order by creation date (newest first)
        query = query.order_by(desc(InstallmentPlan.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        plans = query.offset(offset).limit(size).all()
        
        return plans, total
    
    @staticmethod
    def customer_has_business_interaction(
        db: Session,
        customer_id: str,
        business_id: str
    ) -> bool:
        """Check if customer has any interaction with a specific business"""
        
        # Check for installment requests
        request_exists = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.business_id == business_id
        ).first()
        
        if request_exists:
            return True
        
        # Check for installment plans
        plan_exists = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.business_id == business_id
        ).first()
        
        return plan_exists is not None
    
    @staticmethod
    def _calculate_simple_risk_score(
        active_plans: List[InstallmentPlan],
        completed_plans: List[InstallmentPlan],
        fraud_alerts: List[FraudAlert]
    ) -> float:
        """Calculate a simple risk score based on customer history"""
        
        risk_score = 0.0
        
        # Active plans factor
        if len(active_plans) > 3:
            risk_score += 20
        elif len(active_plans) > 1:
            risk_score += 10
        
        # Completion rate factor
        total_plans = len(active_plans) + len(completed_plans)
        if total_plans > 0:
            completion_rate = len(completed_plans) / total_plans
            if completion_rate < 0.5:
                risk_score += 30
            elif completion_rate < 0.8:
                risk_score += 15
        
        # Fraud alerts factor
        if len(fraud_alerts) > 0:
            risk_score += len(fraud_alerts) * 10
        
        return min(risk_score, 100.0)  # Cap at 100