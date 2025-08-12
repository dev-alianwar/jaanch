"""
Authentication related models
"""
# For now, auth models are in database/models.py
# This file can contain auth-specific model extensions or DTOs

from database.models import User, UserRole

# Re-export for convenience
__all__ = ["User", "UserRole"]

# Future: Add auth-specific model extensions here
# class UserProfile(BaseModel):
#     """Extended user profile information"""
#     pass