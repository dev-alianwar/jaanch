"""
Approval service layer for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
import logging

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    RequestStatus, PlanStatus, PaymentStatus, UserRole
)

logger = logging.getLogger(__name__)

class ApprovalService:
    """Service class for installment request approval operations"""
    
    @staticmethod
    def approve_request(
        db: Session,
        request_id: str,
        business_notes: Optional[str] = None
    ) -> InstallmentPlan:
        """Approve installment request and create installment plan"""
        
        # Get the installment request
        request_obj = db.query(InstallmentRequest).options(
            joinedload(InstallmentRequest.customer),
            joinedload(InstallmentRequest.business)
        ).filter(InstallmentRequest.id == request_id).first()
        
        if not request_obj:
            raise ValueError("Installment request not found")
        
        if request_obj.status != RequestStatus.PENDING:
            raise ValueError("Request is not in pending status")
        
        # Update request status
        request_obj.status = RequestStatus.APPROVED
        request_obj.business_notes = business_notes
        request_obj.updated_at = datetime.utcnow()
        
        # Calculate installment plan details
        start_date = date.today()
        end_date = ApprovalService._calculate_end_date(start_date, request_obj.installment_months)
        
        # Create installment plan
        installment_plan = InstallmentPlan(
            request_id=request_obj.id,
            customer_id=request_obj.customer_id,
            business_id=request_obj.business_id,
            total_amount=request_obj.product_value,
            paid_amount=Decimal('0.00'),
            remaining_amount=request_obj.product_value,
            total_installments=request_obj.installment_months,
            paid_installments=0,
            start_date=start_date,
            end_date=end_date,
            status=PlanStatus.ACTIVE
        )
        
        db.add(installment_plan)
        db.commit()
        db.refresh(installment_plan)
        
        # Generate payment schedule
        PaymentService.generate_payment_schedule(db, installment_plan.id)
        
        # Load relationships for return
        plan_with_relations = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.customer),
            joinedload(InstallmentPlan.business),
            joinedload(InstallmentPlan.payments)
        ).filter(InstallmentPlan.id == installment_plan.id).first()
        
        logger.info(f"Installment request approved and plan created: {installment_plan.id}")
        return plan_with_relations
    
    @staticmethod
    def reject_request(
        db: Session,
        request_id: str,
        business_notes: str
    ) -> bool:
        """Reject installment request"""
        
        request_obj = db.query(InstallmentRequest).filter(
            InstallmentRequest.id == request_id
        ).first()
        
        if not request_obj:
            raise ValueError("Installment request not found")
        
        if request_obj.status != RequestStatus.PENDING:
            raise ValueError("Request is not in pending status")
        
        # Update request status
        request_obj.status = RequestStatus.REJECTED
        request_obj.business_notes = business_notes
        request_obj.updated_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Installment request rejected: {request_id}")
        return True
    
    @staticmethod
    def get_pending_requests_with_history(
        db: Session,
        business_id: str,
        page: int = 1,
        size: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Get pending requests with customer history for business decision making"""
        
        # Base query for pending requests
        query = db.query(InstallmentRequest).options(
            joinedload(InstallmentRequest.customer)
        ).filter(
            InstallmentRequest.business_id == business_id,
            InstallmentRequest.status == RequestStatus.PENDING
        )
        
        # Apply sorting
        sort_column = getattr(InstallmentRequest, sort_by, InstallmentRequest.created_at)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        requests = query.offset(offset).limit(size).all()
        
        # Enhance each request with customer history
        enhanced_requests = []
        for request in requests:
            customer_summary = ApprovalService._get_customer_summary(db, str(request.customer_id))
            
            enhanced_request = {
                "request": {
                    "id": str(request.id),
                    "product_name": request.product_name,
                    "product_description": request.product_description,
                    "product_value": float(request.product_value),
                    "installment_months": request.installment_months,
                    "monthly_amount": float(request.monthly_amount),
                    "created_at": request.created_at.isoformat(),
                    "customer": {
                        "id": str(request.customer.id),
                        "first_name": request.customer.first_name,
                        "last_name": request.customer.last_name,
                        "email": request.customer.email,
                        "phone": request.customer.phone
                    }
                },
                "customer_history": customer_summary
            }
            enhanced_requests.append(enhanced_request)
        
        return enhanced_requests, total
    
    @staticmethod
    def _get_customer_summary(db: Session, customer_id: str) -> Dict[str, Any]:
        """Get customer installment history summary"""
        
        # Get active installment plans
        active_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).all()
        
        # Get completed installment plans
        completed_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.COMPLETED
        ).all()
        
        # Get defaulted plans
        defaulted_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.DEFAULTED
        ).all()
        
        # Calculate totals
        total_active_debt = sum(plan.remaining_amount for plan in active_plans)
        total_completed_amount = sum(plan.total_amount for plan in completed_plans)
        total_defaulted_amount = sum(plan.total_amount for plan in defaulted_plans)
        
        # Get recent request activity (last 30 days)
        recent_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=30)
        ).count()
        
        # Calculate payment history
        payment_stats = ApprovalService._calculate_payment_stats(db, customer_id)
        
        return {
            "active_plans_count": len(active_plans),
            "completed_plans_count": len(completed_plans),
            "defaulted_plans_count": len(defaulted_plans),
            "total_active_debt": float(total_active_debt),
            "total_completed_amount": float(total_completed_amount),
            "total_defaulted_amount": float(total_defaulted_amount),
            "recent_requests_30_days": recent_requests,
            "payment_history": payment_stats,
            "risk_indicators": ApprovalService._calculate_risk_indicators(
                len(active_plans), len(defaulted_plans), recent_requests, payment_stats
            )
        }
    
    @staticmethod
    def _calculate_payment_stats(db: Session, customer_id: str) -> Dict[str, Any]:
        """Calculate customer payment statistics"""
        
        # Get all payments for customer's plans
        payments = db.query(Payment).join(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id
        ).all()
        
        if not payments:
            return {
                "total_payments": 0,
                "on_time_payments": 0,
                "late_payments": 0,
                "missed_payments": 0,
                "payment_reliability": 0.0
            }
        
        total_payments = len(payments)
        on_time_payments = len([p for p in payments if p.status == PaymentStatus.PAID and p.paid_date and p.paid_date <= p.due_date])
        late_payments = len([p for p in payments if p.status == PaymentStatus.PAID and p.paid_date and p.paid_date > p.due_date])
        missed_payments = len([p for p in payments if p.status == PaymentStatus.OVERDUE])
        
        payment_reliability = (on_time_payments / total_payments * 100) if total_payments > 0 else 0
        
        return {
            "total_payments": total_payments,
            "on_time_payments": on_time_payments,
            "late_payments": late_payments,
            "missed_payments": missed_payments,
            "payment_reliability": round(payment_reliability, 2)
        }
    
    @staticmethod
    def _calculate_risk_indicators(
        active_plans: int,
        defaulted_plans: int,
        recent_requests: int,
        payment_stats: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate risk indicators for customer"""
        
        risk_score = 0
        risk_factors = []
        
        # High number of active plans
        if active_plans > 3:
            risk_score += 20
            risk_factors.append("Multiple active installment plans")
        
        # Has defaulted plans
        if defaulted_plans > 0:
            risk_score += 30
            risk_factors.append("History of defaulted payments")
        
        # Too many recent requests
        if recent_requests > 5:
            risk_score += 25
            risk_factors.append("High frequency of recent requests")
        
        # Poor payment reliability
        payment_reliability = payment_stats.get("payment_reliability", 100)
        if payment_reliability < 80:
            risk_score += 15
            risk_factors.append("Poor payment reliability")
        
        # Determine risk level
        if risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 25:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "risk_score": min(risk_score, 100),  # Cap at 100
            "risk_level": risk_level,
            "risk_factors": risk_factors
        }
    
    @staticmethod
    def _calculate_end_date(start_date: date, months: int) -> date:
        """Calculate end date for installment plan"""
        # Simple calculation - add months to start date
        year = start_date.year
        month = start_date.month + months
        
        # Handle year overflow
        while month > 12:
            year += 1
            month -= 12
        
        # Handle day overflow for shorter months
        day = start_date.day
        try:
            end_date = date(year, month, day)
        except ValueError:
            # Day doesn't exist in target month (e.g., Jan 31 -> Feb 31)
            # Use last day of target month
            if month == 2:
                day = 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28
            elif month in [4, 6, 9, 11]:
                day = 30
            else:
                day = 31
            end_date = date(year, month, day)
        
        return end_date
    
    @staticmethod
    def get_business_analytics(db: Session, business_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a business"""
        
        # Get request statistics
        request_stats = db.query(
            func.count(InstallmentRequest.id).label('total_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.PENDING, True)).label('pending'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.REJECTED, True)).label('rejected')
        ).filter(InstallmentRequest.business_id == business_id).first()
        
        # Get plan statistics
        plan_stats = db.query(
            func.count(InstallmentPlan.id).label('total_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.ACTIVE, True)).label('active'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_value'),
            func.coalesce(func.sum(InstallmentPlan.paid_amount), 0).label('total_paid'),
            func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0).label('total_outstanding')
        ).filter(InstallmentPlan.business_id == business_id).first()
        
        # Calculate approval rate
        approval_rate = 0
        if request_stats.total_requests > 0:
            approval_rate = (request_stats.approved / request_stats.total_requests) * 100
        
        # Calculate default rate
        default_rate = 0
        if plan_stats.total_plans > 0:
            default_rate = (plan_stats.defaulted / plan_stats.total_plans) * 100
        
        return {
            "requests": {
                "total": request_stats.total_requests,
                "pending": request_stats.pending,
                "approved": request_stats.approved,
                "rejected": request_stats.rejected,
                "approval_rate": round(approval_rate, 2)
            },
            "plans": {
                "total": plan_stats.total_plans,
                "active": plan_stats.active,
                "completed": plan_stats.completed,
                "defaulted": plan_stats.defaulted,
                "default_rate": round(default_rate, 2)
            },
            "financial": {
                "total_value": float(plan_stats.total_value),
                "total_paid": float(plan_stats.total_paid),
                "total_outstanding": float(plan_stats.total_outstanding),
                "collection_rate": round((float(plan_stats.total_paid) / float(plan_stats.total_value) * 100) if plan_stats.total_value > 0 else 0, 2)
            }
        }

class PaymentService:
    """Service class for payment management"""
    
    @staticmethod
    def generate_payment_schedule(db: Session, plan_id: str) -> List[Payment]:
        """Generate payment schedule for an installment plan"""
        
        plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
        if not plan:
            raise ValueError("Installment plan not found")
        
        payments = []
        monthly_amount = plan.total_amount / plan.total_installments
        
        for i in range(plan.total_installments):
            # Calculate due date (monthly intervals from start date)
            due_date = ApprovalService._calculate_end_date(plan.start_date, i + 1)
            
            payment = Payment(
                plan_id=plan.id,
                amount=monthly_amount,
                due_date=due_date,
                status=PaymentStatus.PENDING
            )
            payments.append(payment)
            db.add(payment)
        
        db.commit()
        
        logger.info(f"Payment schedule generated for plan {plan_id}: {len(payments)} payments")
        return payments
    
    @staticmethod
    def record_payment(
        db: Session,
        plan_id: str,
        amount: Decimal,
        payment_method: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Payment:
        """Record a payment for an installment plan"""
        
        plan = db.query(InstallmentPlan).filter(InstallmentPlan.id == plan_id).first()
        if not plan:
            raise ValueError("Installment plan not found")
        
        if plan.status != PlanStatus.ACTIVE:
            raise ValueError("Cannot record payment for inactive plan")
        
        if amount <= 0:
            raise ValueError("Payment amount must be greater than 0")
        
        if amount > plan.remaining_amount:
            raise ValueError("Payment amount exceeds remaining balance")
        
        # Find the next pending payment or create a new one
        next_payment = db.query(Payment).filter(
            Payment.plan_id == plan_id,
            Payment.status == PaymentStatus.PENDING
        ).order_by(Payment.due_date).first()
        
        if next_payment:
            # Update existing payment
            next_payment.amount = amount
            next_payment.paid_date = date.today()
            next_payment.status = PaymentStatus.PAID
            next_payment.payment_method = payment_method
            next_payment.notes = notes
            payment = next_payment
        else:
            # Create new payment record
            payment = Payment(
                plan_id=plan_id,
                amount=amount,
                due_date=date.today(),
                paid_date=date.today(),
                status=PaymentStatus.PAID,
                payment_method=payment_method,
                notes=notes
            )
            db.add(payment)
        
        # Update plan amounts
        plan.paid_amount += amount
        plan.remaining_amount -= amount
        plan.paid_installments += 1
        
        # Check if plan is completed
        if plan.remaining_amount <= 0:
            plan.status = PlanStatus.COMPLETED
            plan.remaining_amount = Decimal('0.00')  # Ensure it's exactly zero
        
        db.commit()
        db.refresh(payment)
        
        logger.info(f"Payment recorded: {payment.id} for plan {plan_id}")
        return payment