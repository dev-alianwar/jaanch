"""
Customer history service layer for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc, asc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, RequestStatus, PlanStatus, PaymentStatus
)
from schemas import (
    CustomerInstallmentHistory, UserResponse, InstallmentPlanResponse,
    FraudAlertResponse, FraudPatternResponse, PaymentResponse
)

logger = logging.getLogger(__name__)

class HistoryService:
    """Service class for customer installment history operations"""
    
    @staticmethod
    def get_complete_customer_history(db: Session, customer_id: str) -> CustomerInstallmentHistory:
        """Get complete installment history for a customer across all businesses"""
        
        # Get customer
        customer = db.query(User).filter(User.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        # Get active installment plans
        active_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).order_by(desc(InstallmentPlan.created_at)).all()
        
        # Get completed installment plans
        completed_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.COMPLETED
        ).order_by(desc(InstallmentPlan.created_at)).all()
        
        # Get fraud alerts
        fraud_alerts = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id
        ).order_by(desc(FraudAlert.created_at)).all()
        
        # Get fraud patterns
        fraud_patterns = db.query(FraudPattern).filter(
            FraudPattern.customer_id == customer_id
        ).order_by(desc(FraudPattern.detected_at)).all()
        
        # Calculate totals
        total_active_debt = sum(plan.remaining_amount for plan in active_plans)
        total_completed_amount = sum(plan.total_amount for plan in completed_plans)
        
        # Calculate risk score (simplified version)
        risk_score = HistoryService._calculate_simple_risk_score(
            active_plans, completed_plans, fraud_alerts
        )
        
        return CustomerInstallmentHistory(
            customer=UserResponse.from_orm(customer),
            active_plans=[InstallmentPlanResponse.from_orm(plan) for plan in active_plans],
            completed_plans=[InstallmentPlanResponse.from_orm(plan) for plan in completed_plans],
            total_active_debt=total_active_debt,
            total_completed_amount=total_completed_amount,
            fraud_alerts=[FraudAlertResponse.from_orm(alert) for alert in fraud_alerts],
            fraud_patterns=[FraudPatternResponse.from_orm(pattern) for pattern in fraud_patterns],
            risk_score=Decimal(str(risk_score))
        )
    
    @staticmethod
    def get_customer_active_plans(
        db: Session,
        customer_id: str,
        page: int = 1,
        size: int = 10,
        business_filter: Optional[str] = None
    ) -> Tuple[List[InstallmentPlan], int]:
        """Get paginated active installment plans for a customer"""
        
        query = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        )
        
        # Apply business filter if provided
        if business_filter:
            query = query.join(Business).filter(
                Business.business_name.ilike(f"%{business_filter}%")
            )
        
        # Order by creation date (newest first)
        query = query.order_by(desc(InstallmentPlan.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        plans = query.offset(offset).limit(size).all()
        
        return plans, total
    
    @staticmethod
    def get_customer_payment_history(
        db: Session,
        customer_id: str,
        page: int = 1,
        size: int = 10,
        plan_id: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Get paginated payment history for a customer"""
        
        query = db.query(Payment).join(InstallmentPlan).options(
            joinedload(Payment.plan).joinedload(InstallmentPlan.business)
        ).filter(InstallmentPlan.customer_id == customer_id)
        
        # Apply filters
        if plan_id:
            query = query.filter(Payment.plan_id == plan_id)
        
        if date_from:
            query = query.filter(Payment.created_at >= date_from)
        
        if date_to:
            query = query.filter(Payment.created_at <= date_to)
        
        # Order by creation date (newest first)
        query = query.order_by(desc(Payment.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        payments = query.offset(offset).limit(size).all()
        
        # Format response with additional context
        formatted_payments = []
        for payment in payments:
            formatted_payment = {
                "id": str(payment.id),
                "plan_id": str(payment.plan_id),
                "amount": float(payment.amount),
                "due_date": payment.due_date.isoformat() if payment.due_date else None,
                "paid_date": payment.paid_date.isoformat() if payment.paid_date else None,
                "status": payment.status.value,
                "payment_method": payment.payment_method,
                "notes": payment.notes,
                "created_at": payment.created_at.isoformat(),
                "business": {
                    "id": str(payment.plan.business.id),
                    "name": payment.plan.business.business_name,
                    "type": payment.plan.business.business_type
                },
                "plan_info": {
                    "total_amount": float(payment.plan.total_amount),
                    "remaining_amount": float(payment.plan.remaining_amount)
                }
            }
            formatted_payments.append(formatted_payment)
        
        return formatted_payments, total
    
    @staticmethod
    def get_customer_business_relationships(
        db: Session,
        customer_id: str
    ) -> List[Dict[str, Any]]:
        """Get all businesses the customer has had relationships with"""
        
        # Get all installment plans for the customer
        plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner)
        ).filter(InstallmentPlan.customer_id == customer_id).all()
        
        # Group by business
        business_relationships = {}
        for plan in plans:
            business_id = str(plan.business.id)
            if business_id not in business_relationships:
                business_relationships[business_id] = {
                    "business": {
                        "id": business_id,
                        "name": plan.business.business_name,
                        "type": plan.business.business_type,
                        "is_verified": plan.business.is_verified
                    },
                    "relationship_stats": {
                        "total_plans": 0,
                        "active_plans": 0,
                        "completed_plans": 0,
                        "defaulted_plans": 0,
                        "total_amount": 0.0,
                        "paid_amount": 0.0,
                        "remaining_amount": 0.0,
                        "first_plan_date": None,
                        "last_plan_date": None
                    }
                }
            
            # Update statistics
            stats = business_relationships[business_id]["relationship_stats"]
            stats["total_plans"] += 1
            stats["total_amount"] += float(plan.total_amount)
            stats["paid_amount"] += float(plan.paid_amount)
            stats["remaining_amount"] += float(plan.remaining_amount)
            
            if plan.status == PlanStatus.ACTIVE:
                stats["active_plans"] += 1
            elif plan.status == PlanStatus.COMPLETED:
                stats["completed_plans"] += 1
            elif plan.status == PlanStatus.DEFAULTED:
                stats["defaulted_plans"] += 1
            
            # Update dates
            plan_date = plan.created_at.isoformat()
            if not stats["first_plan_date"] or plan_date < stats["first_plan_date"]:
                stats["first_plan_date"] = plan_date
            if not stats["last_plan_date"] or plan_date > stats["last_plan_date"]:
                stats["last_plan_date"] = plan_date
        
        return list(business_relationships.values())
    
    @staticmethod
    def get_customer_statistics(db: Session, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive statistics for a customer"""
        
        # Get plan statistics
        plan_stats = db.query(
            func.count(InstallmentPlan.id).label('total_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.ACTIVE, True)).label('active'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_value'),
            func.coalesce(func.sum(InstallmentPlan.paid_amount), 0).label('total_paid'),
            func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0).label('total_outstanding')
        ).filter(InstallmentPlan.customer_id == customer_id).first()
        
        # Get payment statistics
        payment_stats = db.query(
            func.count(Payment.id).label('total_payments'),
            func.count(func.nullif(Payment.status != PaymentStatus.PAID, True)).label('paid_payments'),
            func.count(func.nullif(Payment.status != PaymentStatus.OVERDUE, True)).label('overdue_payments')
        ).join(InstallmentPlan).filter(InstallmentPlan.customer_id == customer_id).first()
        
        # Get request statistics
        request_stats = db.query(
            func.count(InstallmentRequest.id).label('total_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.REJECTED, True)).label('rejected')
        ).filter(InstallmentRequest.customer_id == customer_id).first()
        
        # Get unique businesses count
        unique_businesses = db.query(func.count(func.distinct(InstallmentPlan.business_id))).filter(
            InstallmentPlan.customer_id == customer_id
        ).scalar()
        
        # Calculate rates
        completion_rate = 0
        if plan_stats.total_plans > 0:
            completion_rate = (plan_stats.completed / plan_stats.total_plans) * 100
        
        payment_reliability = 0
        if payment_stats.total_payments > 0:
            payment_reliability = (payment_stats.paid_payments / payment_stats.total_payments) * 100
        
        approval_rate = 0
        if request_stats.total_requests > 0:
            approval_rate = (request_stats.approved / request_stats.total_requests) * 100
        
        return {
            "customer_id": customer_id,
            "plans": {
                "total": plan_stats.total_plans,
                "active": plan_stats.active,
                "completed": plan_stats.completed,
                "defaulted": plan_stats.defaulted,
                "completion_rate": round(completion_rate, 2)
            },
            "financial": {
                "total_value": float(plan_stats.total_value),
                "total_paid": float(plan_stats.total_paid),
                "total_outstanding": float(plan_stats.total_outstanding),
                "payment_reliability": round(payment_reliability, 2)
            },
            "requests": {
                "total": request_stats.total_requests,
                "approved": request_stats.approved,
                "rejected": request_stats.rejected,
                "approval_rate": round(approval_rate, 2)
            },
            "relationships": {
                "unique_businesses": unique_businesses
            },
            "payments": {
                "total": payment_stats.total_payments,
                "paid": payment_stats.paid_payments,
                "overdue": payment_stats.overdue_payments
            }
        }
    
    @staticmethod
    def get_cross_business_analysis(db: Session, customer_id: str) -> Dict[str, Any]:
        """Get cross-business analysis for fraud detection"""
        
        # Get all plans for the customer
        plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business)
        ).filter(InstallmentPlan.customer_id == customer_id).order_by(
            InstallmentPlan.created_at
        ).all()
        
        if not plans:
            return {
                "customer_id": customer_id,
                "analysis": "No installment history found",
                "risk_indicators": []
            }
        
        # Analyze patterns
        business_sequence = []
        business_switches = 0
        rapid_switches = 0
        
        for i, plan in enumerate(plans):
            business_info = {
                "business_id": str(plan.business.id),
                "business_name": plan.business.business_name,
                "plan_date": plan.created_at.isoformat(),
                "amount": float(plan.total_amount),
                "status": plan.status.value
            }
            business_sequence.append(business_info)
            
            # Check for business switches
            if i > 0 and plan.business_id != plans[i-1].business_id:
                business_switches += 1
                
                # Check for rapid switches (within 30 days)
                time_diff = plan.created_at - plans[i-1].created_at
                if time_diff.days <= 30:
                    rapid_switches += 1
        
        # Calculate risk indicators
        risk_indicators = []
        
        if business_switches > 3:
            risk_indicators.append("High frequency of business switching")
        
        if rapid_switches > 1:
            risk_indicators.append("Rapid business switching pattern detected")
        
        # Check for overlapping active plans
        active_overlaps = HistoryService._check_active_plan_overlaps(plans)
        if active_overlaps > 2:
            risk_indicators.append("Multiple concurrent active plans")
        
        # Check for high-value pattern
        high_value_plans = [p for p in plans if p.total_amount > 10000]
        if len(high_value_plans) > 3:
            risk_indicators.append("Pattern of high-value installments")
        
        return {
            "customer_id": customer_id,
            "total_businesses": len(set(p.business_id for p in plans)),
            "total_plans": len(plans),
            "business_switches": business_switches,
            "rapid_switches": rapid_switches,
            "business_sequence": business_sequence,
            "risk_indicators": risk_indicators,
            "analysis_date": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_customer_timeline(
        db: Session,
        customer_id: str,
        days: int = 90
    ) -> List[Dict[str, Any]]:
        """Get chronological timeline of customer installment activity"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        timeline_events = []
        
        # Get installment requests
        requests = db.query(InstallmentRequest).options(
            joinedload(InstallmentRequest.business)
        ).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= cutoff_date
        ).all()
        
        for request in requests:
            timeline_events.append({
                "date": request.created_at.isoformat(),
                "type": "installment_request",
                "description": f"Requested installment for {request.product_name}",
                "business": request.business.business_name,
                "amount": float(request.product_value),
                "status": request.status.value,
                "details": {
                    "product_name": request.product_name,
                    "installment_months": request.installment_months,
                    "monthly_amount": float(request.monthly_amount)
                }
            })
        
        # Get payments
        payments = db.query(Payment).join(InstallmentPlan).options(
            joinedload(Payment.plan).joinedload(InstallmentPlan.business)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            Payment.created_at >= cutoff_date
        ).all()
        
        for payment in payments:
            timeline_events.append({
                "date": payment.created_at.isoformat(),
                "type": "payment",
                "description": f"Payment of ${payment.amount}",
                "business": payment.plan.business.business_name,
                "amount": float(payment.amount),
                "status": payment.status.value,
                "details": {
                    "due_date": payment.due_date.isoformat() if payment.due_date else None,
                    "paid_date": payment.paid_date.isoformat() if payment.paid_date else None,
                    "payment_method": payment.payment_method
                }
            })
        
        # Get fraud alerts
        alerts = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id,
            FraudAlert.created_at >= cutoff_date
        ).all()
        
        for alert in alerts:
            timeline_events.append({
                "date": alert.created_at.isoformat(),
                "type": "fraud_alert",
                "description": alert.description,
                "business": None,
                "amount": None,
                "status": alert.status.value,
                "details": {
                    "alert_type": alert.alert_type.value,
                    "severity": alert.severity.value,
                    "metadata": alert.alert_metadata
                }
            })
        
        # Sort by date (newest first)
        timeline_events.sort(key=lambda x: x["date"], reverse=True)
        
        return timeline_events
    
    @staticmethod
    def customer_has_business_interaction(
        db: Session,
        customer_id: str,
        business_id: str
    ) -> bool:
        """Check if customer has any interaction with a specific business"""
        
        # Check for installment requests
        request_exists = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.business_id == business_id
        ).first()
        
        if request_exists:
            return True
        
        # Check for installment plans
        plan_exists = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.business_id == business_id
        ).first()
        
        return plan_exists is not None
    
    @staticmethod
    def _calculate_simple_risk_score(
        active_plans: List[InstallmentPlan],
        completed_plans: List[InstallmentPlan],
        fraud_alerts: List[FraudAlert]
    ) -> float:
        """Calculate a simple risk score based on customer history"""
        
        risk_score = 0.0
        
        # Active plans factor
        if len(active_plans) > 3:
            risk_score += 20
        elif len(active_plans) > 1:
            risk_score += 10
        
        # Completion rate factor
        total_plans = len(active_plans) + len(completed_plans)
        if total_plans > 0:
            completion_rate = len(completed_plans) / total_plans
            if completion_rate < 0.5:
                risk_score += 30
            elif completion_rate < 0.8:
                risk_score += 15
        
        # Fraud alerts factor
        if len(fraud_alerts) > 0:
            risk_score += len(fraud_alerts) * 10
        
        return min(risk_score, 100.0)  # Cap at 100
    
    @staticmethod
    def _check_active_plan_overlaps(plans: List[InstallmentPlan]) -> int:
        """Check for overlapping active installment plans"""
        
        active_periods = []
        for plan in plans:
            if plan.status == PlanStatus.ACTIVE:
                active_periods.append((plan.start_date, plan.end_date))
        
        # Count overlaps
        overlaps = 0
        for i in range(len(active_periods)):
            for j in range(i + 1, len(active_periods)):
                start1, end1 = active_periods[i]
                start2, end2 = active_periods[j]
                
                # Check if periods overlap
                if start1 <= end2 and start2 <= end1:
                    overlaps += 1
        
        return overlaps