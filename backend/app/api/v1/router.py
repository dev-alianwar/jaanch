"""
Main API v1 router
"""
from fastapi import APIRouter
from .auth import router as auth_router

# Create main v1 router
api_router = APIRouter(prefix="/api/v1")

# Include sub-routers
api_router.include_router(auth_router)

# Add other routers here as they are created
# api_router.include_router(users_router)
# api_router.include_router(installments_router)
# api_router.include_router(fraud_router)