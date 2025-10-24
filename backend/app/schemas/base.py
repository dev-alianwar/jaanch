"""
Base schemas for common functionality
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    class Config:
        from_attributes = True
        use_enum_values = True


class TimestampMixin(BaseModel):
    """Mixin for models with timestamps"""
    created_at: datetime
    updated_at: Optional[datetime] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    size: int = 20
    
    class Config:
        schema_extra = {
            "example": {
                "page": 1,
                "size": 20
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: list
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "size": 20,
                "pages": 5
            }
        }