"""
Installment related schemas
"""
import uuid
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from pydantic import Field
from .base import BaseSchema
from .auth import UserResponse
from database.models import RequestStatus


class InstallmentRequestCreate(BaseSchema):
    """Schema for creating installment requests"""
    business_id: uuid.UUID
    product_name: str = Field(..., min_length=1, max_length=255)
    product_description: Optional[str] = None
    product_value: Decimal = Field(..., gt=0)
    installment_months: int = Field(..., gt=0, le=60)


class InstallmentRequestUpdate(BaseSchema):
    """Schema for updating installment requests"""
    product_name: Optional[str] = Field(None, min_length=1, max_length=255)
    product_description: Optional[str] = None
    product_value: Optional[Decimal] = Field(None, gt=0)
    installment_months: Optional[int] = Field(None, gt=0, le=60)


class BusinessResponse(BaseSchema):
    """Business response schema"""
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


class InstallmentRequestResponse(BaseSchema):
    """Installment request response schema"""
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


class RequestApproval(BaseSchema):
    """Schema for approving requests"""
    business_notes: Optional[str] = None


class RequestRejection(BaseSchema):
    """Schema for rejecting requests"""
    business_notes: str = Field(..., min_length=1)


class PaginatedResponse(BaseSchema):
    """Generic paginated response"""
    items: list
    total: int
    page: int
    size: int
    pages: int