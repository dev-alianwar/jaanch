from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum
from datetime import datetime, date
from typing import Optional

# Enum definitions
class UserRole(str, enum.Enum):
    SUPERADMIN = "superadmin"
    BUSINESS = "business"
    CUSTOMER = "customer"

class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PlanStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class AlertType(str, enum.Enum):
    RAPID_REQUESTS = "rapid_requests"
    HIGH_DEBT_RATIO = "high_debt_ratio"
    CROSS_BUSINESS_CHAIN = "cross_business_chain"
    PAYMENT_DEFAULT_PATTERN = "payment_default_pattern"

class AlertSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertStatus(str, enum.Enum):
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

# Model definitions
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)

    # Relationships
    businesses = relationship("Business", back_populates="owner", cascade="all, delete-orphan")
    installment_requests = relationship("InstallmentRequest", back_populates="customer", cascade="all, delete-orphan")
    installment_plans = relationship("InstallmentPlan", back_populates="customer", cascade="all, delete-orphan")
    fraud_alerts = relationship("FraudAlert", back_populates="customer", cascade="all, delete-orphan")
    fraud_patterns = relationship("FraudPattern", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"

class Business(Base):
    __tablename__ = "businesses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    business_name = Column(String(255), nullable=False)
    business_type = Column(String(100))
    address = Column(Text)
    phone = Column(String(20))
    registration_number = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=False, index=True)

    # Relationships
    owner = relationship("User", back_populates="businesses")
    installment_requests = relationship("InstallmentRequest", back_populates="business", cascade="all, delete-orphan")
    installment_plans = relationship("InstallmentPlan", back_populates="business", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Business(id={self.id}, name={self.business_name})>"

class InstallmentRequest(Base):
    __tablename__ = "installment_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    product_name = Column(String(255), nullable=False)
    product_description = Column(Text)
    product_value = Column(Numeric(12, 2), nullable=False)
    installment_months = Column(Integer, nullable=False)
    monthly_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(SQLEnum(RequestStatus), default=RequestStatus.PENDING, index=True)
    business_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    customer = relationship("User", back_populates="installment_requests")
    business = relationship("Business", back_populates="installment_requests")
    installment_plan = relationship("InstallmentPlan", back_populates="request", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InstallmentRequest(id={self.id}, product={self.product_name}, status={self.status})>"

class InstallmentPlan(Base):
    __tablename__ = "installment_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("installment_requests.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True)
    total_amount = Column(Numeric(12, 2), nullable=False)
    paid_amount = Column(Numeric(12, 2), default=0)
    remaining_amount = Column(Numeric(12, 2), nullable=False)
    total_installments = Column(Integer, nullable=False)
    paid_installments = Column(Integer, default=0)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    status = Column(SQLEnum(PlanStatus), default=PlanStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    request = relationship("InstallmentRequest", back_populates="installment_plan")
    customer = relationship("User", back_populates="installment_plans")
    business = relationship("Business", back_populates="installment_plans")
    payments = relationship("Payment", back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InstallmentPlan(id={self.id}, total_amount={self.total_amount}, status={self.status})>"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("installment_plans.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    due_date = Column(Date, nullable=False, index=True)
    paid_date = Column(Date)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, index=True)
    payment_method = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    plan = relationship("InstallmentPlan", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    description = Column(Text, nullable=False)
    alert_metadata = Column(JSONB)
    severity = Column(SQLEnum(AlertSeverity), nullable=False)
    status = Column(SQLEnum(AlertStatus), default=AlertStatus.ACTIVE, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved_at = Column(DateTime(timezone=True))

    # Relationships
    customer = relationship("User", back_populates="fraud_alerts")

    def __repr__(self):
        return f"<FraudAlert(id={self.id}, type={self.alert_type}, severity={self.severity})>"

class FraudPattern(Base):
    __tablename__ = "fraud_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    pattern_type = Column(String(100), nullable=False, index=True)
    pattern_data = Column(JSONB, nullable=False)
    risk_score = Column(Numeric(3, 2), nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    customer = relationship("User", back_populates="fraud_patterns")

    def __repr__(self):
        return f"<FraudPattern(id={self.id}, type={self.pattern_type}, risk_score={self.risk_score})>"