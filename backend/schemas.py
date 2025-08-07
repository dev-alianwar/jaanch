"""
Pydantic schemas for the Installment Fraud Detection System
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from models import UserRole, RequestStatus, PlanStatus, PaymentStatus, AlertType, AlertSeverity, AlertStatus
import uuid

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        use_enum_values = True

# Authentication schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.CUSTOMER

class UserResponse(BaseSchema):
    id: uuid.UUID
    email: str
    role: UserRole
    first_name: str
    last_name: str
    phone: Optional[str]
    created_at: datetime
    is_active: bool

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)

# Business schemas
class BusinessCreate(BaseModel):
    business_name: str = Field(..., min_length=1, max_length=255)
    business_type: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    registration_number: Optional[str] = Field(None, max_length=100)

class BusinessUpdate(BaseModel):
    business_name: Optional[str] = Field(None, min_length=1, max_length=255)
    business_type: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    phone: Optional[str] = Field(None, max_length=20)
    registration_number: Optional[str] = Field(None, max_length=100)

class BusinessResponse(BaseSchema):
    id: uuid.UUID
    owner_id: uuid.UUID
    business_name: str
    business_type: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    registration_number: Optional[str]
    created_at: datetime
    is_verified: bool
    owner: UserResponse

# Installment Request schemas
class InstallmentRequestCreate(BaseModel):
    business_id: uuid.UUID
    product_name: str = Field(..., min_length=1, max_length=255)
    product_description: Optional[str] = None
    product_value: Decimal = Field(..., gt=0, decimal_places=2)
    installment_months: int = Field(..., gt=0, le=60)
    
    @validator('monthly_amount', pre=True, always=True)
    def calculate_monthly_amount(cls, v, values):
        if 'product_value' in values and 'installment_months' in values:
            return values['product_value'] / values['installment_months']
        return v

class InstallmentRequestUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    product_description: Optional[str] = None
    product_value: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    installment_months: Optional[int] = Field(None, gt=0, le=60)

class InstallmentRequestResponse(BaseSchema):
    id: uuid.UUID
    customer_id: uuid.UUID
    business_id: uuid.UUID
    product_name: str
    product_description: Optional[str]
    product_value: Decimal
    installment_months: int
    monthly_amount: Decimal
    status: RequestStatus
    business_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    customer: UserResponse
    business: BusinessResponse

class RequestApproval(BaseModel):
    business_notes: Optional[str] = None

class RequestRejection(BaseModel):
    business_notes: str = Field(..., min_length=1)

# Installment Plan schemas
class InstallmentPlanResponse(BaseSchema):
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
    customer: UserResponse
    business: BusinessResponse

# Payment schemas
class PaymentCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    payment_method: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None

class PaymentResponse(BaseSchema):
    id: uuid.UUID
    plan_id: uuid.UUID
    amount: Decimal
    due_date: date
    paid_date: Optional[date]
    status: PaymentStatus
    payment_method: Optional[str]
    notes: Optional[str]
    created_at: datetime

# Fraud Alert schemas
class FraudAlertResponse(BaseSchema):
    id: uuid.UUID
    customer_id: uuid.UUID
    alert_type: AlertType
    description: str
    alert_metadata: Optional[Dict[str, Any]]
    severity: AlertSeverity
    status: AlertStatus
    created_at: datetime
    resolved_at: Optional[datetime]
    customer: UserResponse

class FraudAlertUpdate(BaseModel):
    status: AlertStatus
    resolved_at: Optional[datetime] = None

# Fraud Pattern schemas
class FraudPatternResponse(BaseSchema):
    id: uuid.UUID
    customer_id: uuid.UUID
    pattern_type: str
    pattern_data: Dict[str, Any]
    risk_score: Decimal
    detected_at: datetime
    customer: UserResponse

# Customer History schemas
class CustomerInstallmentHistory(BaseModel):
    customer: UserResponse
    active_plans: List[InstallmentPlanResponse]
    completed_plans: List[InstallmentPlanResponse]
    total_active_debt: Decimal
    total_completed_amount: Decimal
    fraud_alerts: List[FraudAlertResponse]
    fraud_patterns: List[FraudPatternResponse]
    risk_score: Decimal

# Dashboard schemas
class SystemStatistics(BaseModel):
    total_users: int
    total_businesses: int
    total_customers: int
    total_installment_requests: int
    total_active_plans: int
    total_fraud_alerts: int
    total_debt_amount: Decimal
    fraud_detection_rate: float

class BusinessMetrics(BaseModel):
    business_id: uuid.UUID
    business_name: str
    total_requests: int
    approved_requests: int
    rejected_requests: int
    active_plans: int
    total_revenue: Decimal
    default_rate: float

class FraudTrends(BaseModel):
    period: str
    total_alerts: int
    alerts_by_type: Dict[str, int]
    alerts_by_severity: Dict[str, int]
    top_risk_customers: List[Dict[str, Any]]

# Error schemas
class ErrorResponse(BaseModel):
    error: Dict[str, Any]

class ValidationError(BaseModel):
    field: str
    message: str

# Pagination schemas
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int