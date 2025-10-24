"""
Authentication schemas for request/response validation
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from database import UserRole


class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    role: UserRole
    is_active: bool
    
    @validator('id', pre=True)
    def convert_uuid_to_string(cls, v):
        if hasattr(v, '__str__'):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response schema"""
    user: UserResponse
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Token refresh schema"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"