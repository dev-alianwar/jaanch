"""
Authentication and Authorization system for Installment Fraud Detection
"""
import os
import redis
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from models import User, UserRole
from database import get_db
import logging

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Redis connection for session management
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Redis connection established")
except Exception as e:
    logger.warning(f"Redis connection failed: {e}. Session management will be limited.")
    redis_client = None

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()

class AuthService:
    """Authentication service for JWT token management"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None
    
    @staticmethod
    def store_session(user_id: str, token: str, expires_in: int) -> bool:
        """Store user session in Redis"""
        if not redis_client:
            return True  # Skip if Redis is not available
        
        try:
            session_key = f"session:{user_id}"
            session_data = {
                "token": token,
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(seconds=expires_in)).isoformat()
            }
            redis_client.hset(session_key, mapping=session_data)
            redis_client.expire(session_key, expires_in)
            return True
        except Exception as e:
            logger.error(f"Failed to store session: {e}")
            return False
    
    @staticmethod
    def get_session(user_id: str) -> Optional[Dict[str, Any]]:
        """Get user session from Redis"""
        if not redis_client:
            return None
        
        try:
            session_key = f"session:{user_id}"
            session_data = redis_client.hgetall(session_key)
            return session_data if session_data else None
        except Exception as e:
            logger.error(f"Failed to get session: {e}")
            return None
    
    @staticmethod
    def invalidate_session(user_id: str) -> bool:
        """Invalidate user session"""
        if not redis_client:
            return True
        
        try:
            session_key = f"session:{user_id}"
            redis_client.delete(session_key)
            return True
        except Exception as e:
            logger.error(f"Failed to invalidate session: {e}")
            return False

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user:
        return None
    
    if not AuthService.verify_password(password, user.password_hash):
        return None
    
    return user

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
        payload = AuthService.verify_token(token)
        
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
        
        # Check session validity (if Redis is available)
        session = AuthService.get_session(str(user.id))
        if session and session.get("token") != token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or invalid"
            )
        
        return user
        
    except JWTError:
        raise credentials_exception

def require_role(allowed_roles: list[UserRole]):
    """Decorator to require specific user roles"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Role-specific dependencies
def get_current_superadmin(current_user: User = Depends(require_role([UserRole.SUPERADMIN]))) -> User:
    """Get current superadmin user"""
    return current_user

def get_current_business(current_user: User = Depends(require_role([UserRole.BUSINESS, UserRole.SUPERADMIN]))) -> User:
    """Get current business user (or superadmin)"""
    return current_user

def get_current_customer(current_user: User = Depends(require_role([UserRole.CUSTOMER, UserRole.SUPERADMIN]))) -> User:
    """Get current customer user (or superadmin)"""
    return current_user

def get_current_business_or_customer(current_user: User = Depends(require_role([UserRole.BUSINESS, UserRole.CUSTOMER, UserRole.SUPERADMIN]))) -> User:
    """Get current business or customer user (or superadmin)"""
    return current_user

# Rate limiting utilities
class RateLimiter:
    """Simple rate limiter using Redis"""
    
    @staticmethod
    def is_rate_limited(key: str, limit: int, window: int) -> bool:
        """Check if a key is rate limited"""
        if not redis_client:
            return False  # Skip rate limiting if Redis is not available
        
        try:
            current = redis_client.get(key)
            if current is None:
                redis_client.setex(key, window, 1)
                return False
            
            if int(current) >= limit:
                return True
            
            redis_client.incr(key)
            return False
            
        except Exception as e:
            logger.error(f"Rate limiting check failed: {e}")
            return False  # Allow request if rate limiting fails
    
    @staticmethod
    def get_rate_limit_info(key: str) -> Dict[str, Any]:
        """Get rate limit information for a key"""
        if not redis_client:
            return {"requests": 0, "ttl": 0}
        
        try:
            requests = redis_client.get(key) or 0
            ttl = redis_client.ttl(key)
            return {"requests": int(requests), "ttl": ttl}
        except Exception as e:
            logger.error(f"Failed to get rate limit info: {e}")
            return {"requests": 0, "ttl": 0}

def rate_limit(limit: int = 10, window: int = 60):
    """Rate limiting decorator"""
    def rate_limit_decorator(current_user: User = Depends(get_current_user)):
        key = f"rate_limit:{current_user.id}"
        if RateLimiter.is_rate_limited(key, limit, window):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )
        return current_user
    return rate_limit_decorator