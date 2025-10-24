"""
API dependencies for authentication and authorization
"""
from typing import List
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db, User, UserRole
from app.core.security import SecurityService
from app.core.logging import get_logger

logger = get_logger("dependencies")
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = SecurityService.verify_token(token)
        
        if payload is None:
            raise credentials_exception
        
        # Check token type
        if payload.get("type") != "access":
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Get user from database
        user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
        if user is None:
            raise credentials_exception
        
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise credentials_exception


def require_roles(allowed_roles: List[UserRole]):
    """Dependency to require specific user roles"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


# Role-specific dependencies
def get_current_superadmin(current_user: User = Depends(require_roles([UserRole.SUPERADMIN]))) -> User:
    """Get current superadmin user"""
    return current_user


def get_current_business(current_user: User = Depends(require_roles([UserRole.BUSINESS, UserRole.SUPERADMIN]))) -> User:
    """Get current business user (or superadmin)"""
    return current_user


def get_current_customer(current_user: User = Depends(require_roles([UserRole.CUSTOMER, UserRole.SUPERADMIN]))) -> User:
    """Get current customer user (or superadmin)"""
    return current_user