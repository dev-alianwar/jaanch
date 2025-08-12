"""
History related models
"""
# For now, history models are in database/models.py
# This file can contain history-specific model extensions or DTOs

from database.models import (
    InstallmentPlan, Payment, FraudAlert, FraudPattern,
    PlanStatus, PaymentStatus, AlertType, AlertSeverity, AlertStatus
)

# Re-export for convenience
__all__ = [
    "InstallmentPlan", "Payment", "FraudAlert", "FraudPattern",
    "PlanStatus", "PaymentStatus", "AlertType", "AlertSeverity", "AlertStatus"
]

# Future: Add history-specific model extensions here
# class CustomerSummary(BaseModel):
#     """Customer history summary"""
#     pass