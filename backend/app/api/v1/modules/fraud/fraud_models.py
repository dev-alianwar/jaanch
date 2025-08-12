"""
Fraud detection related models
"""
# For now, fraud models are in database/models.py
# This file can contain fraud-specific model extensions or DTOs

from database.models import (
    FraudAlert, FraudPattern, AlertType, AlertSeverity, AlertStatus
)

# Re-export for convenience
__all__ = [
    "FraudAlert", "FraudPattern", "AlertType", "AlertSeverity", "AlertStatus"
]

# Future: Add fraud-specific model extensions here
# class RiskAssessment(BaseModel):
#     """Risk assessment calculation"""
#     pass