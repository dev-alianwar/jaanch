from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import os
import logging
import uvicorn

# Import our modules
from database import create_tables
from database_utils import init_database, check_database_connection
import translation_models  # Import to register models
from auth_routes import router as auth_router
from user_routes import router as user_router
from installment_routes import router as installment_router
from approval_routes import router as approval_router
from history_routes import router as history_router
from fraud_routes import router as fraud_router
from admin_routes import router as admin_router
from translation_routes import router as translation_router
from models import UserRole

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Installment Fraud Detection System...")
    
    # Run startup sequence
    from startup import startup_sequence
    if not startup_sequence():
        logger.error("Startup sequence failed!")
        raise Exception("Startup sequence failed")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Installment Fraud Detection System",
    description="A comprehensive system to track installment purchases and detect fraudulent chains",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", '["http://localhost:3000", "http://localhost:19006"]')
try:
    import json
    cors_origins = json.loads(CORS_ORIGINS)
except:
    cors_origins = ["http://localhost:3000", "http://localhost:19006"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(installment_router)
app.include_router(approval_router)
app.include_router(history_router)
app.include_router(fraud_router)
app.include_router(admin_router)
app.include_router(translation_router)

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Installment Fraud Detection System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = check_database_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": str(datetime.utcnow())
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error",
                "timestamp": str(datetime.utcnow())
            }
        }
    )

# Development endpoints (remove in production)
if os.getenv("DEBUG", "false").lower() == "true":
    @app.get("/debug/info")
    async def debug_info():
        """Debug information endpoint"""
        return {
            "environment": os.environ.get("ENVIRONMENT", "development"),
            "database_url": os.environ.get("DATABASE_URL", "not set"),
            "redis_url": os.environ.get("REDIS_URL", "not set"),
            "cors_origins": cors_origins
        }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )