"""
Main API v1 router
"""
from fastapi import APIRouter
from .modules.auth.auth_routes import router as auth_router
from .modules.installments.installment_routes import router as installments_router
from .modules.history.history_routes import router as history_router

# Create main v1 router
api_router = APIRouter(prefix="/api/v1")

# Include module routers
api_router.include_router(auth_router)
api_router.include_router(installments_router)
api_router.include_router(history_router)

# Add other module routers here as they are created
# api_router.include_router(fraud_router)
# api_router.include_router(admin_router)