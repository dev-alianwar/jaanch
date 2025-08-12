"""
History related schemas
"""
import uuid
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from .base import BaseSchema
from .auth import UserResponse
from .installment import PaginatedResponse
from database.models import PlanStatus, PaymentStatus, AlertType, AlertSeverity, AlertStatus


class InstallmentPlanResponse(BaseSchema):
    """Installment plan response schema"""
    id: uuid.UUID
    request_id: uuid.UUID
    customer_id: uuid.UUID
    business_id: uuid.UUID
    total_amount: Decimal
    paid_amount: Decimal
    remaining_amount: Decimal
    total_installments: int
    paid_installments: int
    start_date: date
    end_date: date
    status: PlanStatus
    created_at: datetime


class PaymentResponse(BaseSchema):
    """Payment response schema"""
    id: uuid.UUID
    plan_id: uuid.UUID
    amount: Decimal
    due_date: date
    paid_date: Optional[date]
    status: PaymentStatus
    payment_method: Optional[str]
    notes: Optional[str]
    created_at: datetime


class FraudAlertResponse(BaseSchema):
    """Fraud alert response schema"""
    id: uuid.UUID
    customer_id: uuid.UUID
    alert_type: AlertType
    description: str
    alert_metadata: Optional[dict]
    severity: AlertSeverity
    status: AlertStatus
    created_at: datetime
    resolved_at: Optional[datetime]


class FraudPatternResponse(BaseSchema):
    """Fraud pattern response schema"""
    id: uuid.UUID
    customer_id: uuid.UUID
    pattern_type: str
    pattern_data: dict
    risk_score: Decimal
    detected_at: datetime


class CustomerInstallmentHistory(BaseSchema):
    """Complete customer installment history"""
    customer: UserResponse
    active_plans: List[InstallmentPlanResponse]
    completed_plans: List[InstallmentPlanResponse]
    total_active_debt: Decimal
    total_completed_amount: Decimal
    fraud_alerts: List[FraudAlertResponse]
    fraud_patterns: List[FraudPatternResponse]
    risk_score: Decimal