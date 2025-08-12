"""
Input validation utilities for the Installment Fraud Detection System
"""
import re
from typing import Optional, Dict, Any
from pydantic import validator, EmailStr
import logging

logger = logging.getLogger(__name__)

class ValidationUtils:
    """Utility class for input validation"""
    
    @staticmethod
    def validate_phone(phone: Optional[str]) -> Optional[str]:
        """Validate and format phone number"""
        if not phone:
            return None
        
        # Remove all non-digit characters
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Basic phone number validation (international format)
        if not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', phone):
            raise ValueError("Invalid phone number format")
        
        return cleaned
    
    @staticmethod
    def validate_business_name(name: str) -> str:
        """Validate business name"""
        if not name or len(name.strip()) < 2:
            raise ValueError("Business name must be at least 2 characters long")
        
        if len(name) > 255:
            raise ValueError("Business name must be less than 255 characters")
        
        # Check for potentially harmful characters
        if re.search(r'[<>"\']', name):
            raise ValueError("Business name contains invalid characters")
        
        return name.strip()
    
    @staticmethod
    def validate_registration_number(reg_number: Optional[str]) -> Optional[str]:
        """Validate business registration number"""
        if not reg_number:
            return None
        
        # Basic alphanumeric validation
        if not re.match(r'^[A-Za-z0-9\-_]{3,50}$', reg_number):
            raise ValueError("Invalid registration number format")
        
        return reg_number.upper()
    
    @staticmethod
    def sanitize_search_query(query: Optional[str]) -> Optional[str]:
        """Sanitize search query to prevent injection attacks"""
        if not query:
            return None
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\';\\]', '', query)
        
        # Limit length
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        
        return sanitized.strip() if sanitized.strip() else None
    
    @staticmethod
    def validate_user_role(role: str, current_user_role: str) -> bool:
        """Validate if current user can assign the specified role"""
        from models import UserRole
        
        # Only superadmins can create other superadmins
        if role == UserRole.SUPERADMIN.value and current_user_role != UserRole.SUPERADMIN.value:
            return False
        
        return True
    
    @staticmethod
    def validate_update_permissions(
        target_user_role: str, 
        current_user_role: str, 
        update_fields: Dict[str, Any]
    ) -> bool:
        """Validate if current user can update the specified fields"""
        from models import UserRole
        
        # Superadmins can update anything
        if current_user_role == UserRole.SUPERADMIN.value:
            return True
        
        # Users can only update their own basic profile fields
        allowed_fields = {'first_name', 'last_name', 'phone'}
        restricted_fields = {'role', 'is_active', 'email', 'password_hash'}
        
        # Check if trying to update restricted fields
        if any(field in restricted_fields for field in update_fields.keys()):
            return False
        
        # Check if all fields are allowed
        return all(field in allowed_fields for field in update_fields.keys())

class BusinessValidators:
    """Validators specific to business operations"""
    
    @staticmethod
    def validate_business_type(business_type: Optional[str]) -> Optional[str]:
        """Validate business type"""
        if not business_type:
            return None
        
        # List of allowed business types
        allowed_types = [
            'retail', 'electronics', 'clothing', 'furniture', 'automotive',
            'jewelry', 'appliances', 'sports', 'books', 'toys', 'other'
        ]
        
        business_type_lower = business_type.lower().strip()
        
        if business_type_lower not in allowed_types:
            # Allow custom types but validate format
            if not re.match(r'^[A-Za-z\s]{2,50}$', business_type):
                raise ValueError("Invalid business type format")
        
        return business_type.strip().title()
    
    @staticmethod
    def validate_address(address: Optional[str]) -> Optional[str]:
        """Validate business address"""
        if not address:
            return None
        
        if len(address.strip()) < 10:
            raise ValueError("Address must be at least 10 characters long")
        
        if len(address) > 500:
            raise ValueError("Address must be less than 500 characters")
        
        # Basic sanitization
        sanitized = re.sub(r'[<>"\']', '', address)
        
        return sanitized.strip()

class InstallmentValidators:
    """Validators specific to installment operations"""
    
    @staticmethod
    def validate_product_name(product_name: str) -> str:
        """Validate product name"""
        if not product_name or len(product_name.strip()) < 1:
            raise ValueError("Product name is required")
        
        if len(product_name) > 255:
            raise ValueError("Product name must be less than 255 characters")
        
        # Check for potentially harmful characters
        if re.search(r'[<>"\']', product_name):
            raise ValueError("Product name contains invalid characters")
        
        return product_name.strip()
    
    @staticmethod
    def validate_product_value(product_value: float) -> float:
        """Validate product value"""
        if product_value <= 0:
            raise ValueError("Product value must be greater than 0")
        
        if product_value > 1000000:  # 1 million limit
            raise ValueError("Product value exceeds maximum limit of 1,000,000")
        
        # Check for reasonable decimal places
        if len(str(product_value).split('.')[-1]) > 2:
            raise ValueError("Product value can have at most 2 decimal places")
        
        return round(product_value, 2)
    
    @staticmethod
    def validate_installment_months(months: int) -> int:
        """Validate installment months"""
        if months < 1:
            raise ValueError("Installment months must be at least 1")
        
        if months > 60:
            raise ValueError("Installment months cannot exceed 60")
        
        return months
    
    @staticmethod
    def validate_monthly_payment_ratio(product_value: float, months: int) -> bool:
        """Validate that monthly payment is reasonable"""
        monthly_amount = product_value / months
        
        # Minimum monthly payment should be at least $10
        if monthly_amount < 10:
            raise ValueError("Monthly payment amount is too low (minimum $10)")
        
        return True
    
    @staticmethod
    def check_request_frequency(customer_id: str, recent_count: int) -> bool:
        """Check if customer is making too many requests"""
        max_requests_per_day = 5
        
        if recent_count >= max_requests_per_day:
            raise ValueError(f"Too many requests today. Maximum {max_requests_per_day} requests per day allowed")
        
        return True

class SecurityValidators:
    """Security-related validators"""
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if len(password) > 128:
            raise ValueError("Password must be less than 128 characters")
        
        # Check for at least one uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
        
        return True
    
    @staticmethod
    def validate_email_domain(email: str) -> bool:
        """Validate email domain (optional additional security)"""
        # List of blocked domains (example)
        blocked_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com'
        ]
        
        domain = email.split('@')[1].lower() if '@' in email else ''
        
        if domain in blocked_domains:
            raise ValueError("Email domain is not allowed")
        
        return True
    
    @staticmethod
    def check_suspicious_patterns(text: str) -> bool:
        """Check for suspicious patterns in text input"""
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JavaScript protocol
            r'on\w+\s*=',               # Event handlers
            r'<iframe.*?>',             # Iframe tags
            r'eval\s*\(',               # Eval function
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"Suspicious pattern detected: {pattern}")
                return False
        
        return True