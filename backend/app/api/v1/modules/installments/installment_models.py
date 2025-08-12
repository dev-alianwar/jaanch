"""
Installment related models
"""
# For now, installment models are in database/models.py
# This file can contain installment-specific model extensions or DTOs

from database.models import (
    InstallmentRequest, InstallmentPlan, Payment, Business,
    RequestStatus, PlanStatus, PaymentStatus
)

# Re-export for convenience
__all__ = [
    "InstallmentRequest", "InstallmentPlan", "Payment", "Business",
    "RequestStatus", "PlanStatus", "PaymentStatus"
]

# Future: Add installment-specific model extensions here
# class InstallmentCalculation(BaseModel):
#     """Installment calculation helper"""
#     pass