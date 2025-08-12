"""
Fraud detection service for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, AlertType, AlertSeverity, AlertStatus,
    RequestStatus, PlanStatus, PaymentStatus
)
from schemas import CustomerInstallmentHistory, UserResponse

logger = logging.getLogger(__name__)

class FraudDetectionService:
    """Service class for fraud detection and analysis"""
    
    @staticmethod
    def get_customer_complete_history(db: Session, customer_id: str) -> CustomerInstallmentHistory:
        """Get complete installment history for fraud analysis"""
        
        # Get customer
        customer = db.query(User).filter(User.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        # Get active plans
        active_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).all()
        
        # Get completed plans
        completed_plans = db.query(InstallmentPlan).options(
            joinedload(InstallmentPlan.business).joinedload(Business.owner),
            joinedload(InstallmentPlan.payments)
        ).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.COMPLETED
        ).all()
        
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
        
        # Calculate risk score
        risk_score = FraudDetectionService.calculate_customer_risk_score(db, customer_id)
        
        return CustomerInstallmentHistory(
            customer=UserResponse.from_orm(customer),
            active_plans=[plan for plan in active_plans],
            completed_plans=[plan for plan in completed_plans],
            total_active_debt=total_active_debt,
            total_completed_amount=total_completed_amount,
            fraud_alerts=[alert for alert in fraud_alerts],
            fraud_patterns=[pattern for pattern in fraud_patterns],
            risk_score=Decimal(str(risk_score.get('risk_score', 0)))
        )
    
    @staticmethod
    def calculate_customer_risk_score(db: Session, customer_id: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score for a customer"""
        
        risk_score = 0
        risk_factors = []
        risk_details = {}
        
        # 1. Check for rapid requests pattern
        rapid_requests = FraudDetectionService._check_rapid_requests(db, customer_id)
        if rapid_requests['is_suspicious']:
            risk_score += rapid_requests['risk_points']
            risk_factors.append("Rapid request pattern detected")
            risk_details['rapid_requests'] = rapid_requests
        
        # 2. Check for high debt ratio
        debt_ratio = FraudDetectionService._check_debt_ratio(db, customer_id)
        if debt_ratio['is_suspicious']:
            risk_score += debt_ratio['risk_points']
            risk_factors.append("High debt-to-income ratio")
            risk_details['debt_ratio'] = debt_ratio
        
        # 3. Check for cross-business chain pattern
        cross_business = FraudDetectionService._check_cross_business_pattern(db, customer_id)
        if cross_business['is_suspicious']:
            risk_score += cross_business['risk_points']
            risk_factors.append("Cross-business installment chain")
            risk_details['cross_business'] = cross_business
        
        # 4. Check payment default pattern
        payment_defaults = FraudDetectionService._check_payment_defaults(db, customer_id)
        if payment_defaults['is_suspicious']:
            risk_score += payment_defaults['risk_points']
            risk_factors.append("Payment default pattern")
            risk_details['payment_defaults'] = payment_defaults
        
        # 5. Check for unusual product patterns
        product_patterns = FraudDetectionService._check_product_patterns(db, customer_id)
        if product_patterns['is_suspicious']:
            risk_score += product_patterns['risk_points']
            risk_factors.append("Unusual product selection pattern")
            risk_details['product_patterns'] = product_patterns
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Generate recommendations
        recommendations = FraudDetectionService._generate_recommendations(risk_level, risk_factors)
        
        return {
            "customer_id": customer_id,
            "risk_score": min(risk_score, 100),  # Cap at 100
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "risk_details": risk_details,
            "recommendations": recommendations,
            "last_updated": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _check_rapid_requests(db: Session, customer_id: str) -> Dict[str, Any]:
        """Check for rapid request patterns"""
        
        # Check requests in last 24 hours
        recent_24h = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).count()
        
        # Check requests in last 7 days
        recent_7d = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Check requests in last 30 days
        recent_30d = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=30)
        ).count()
        
        is_suspicious = False
        risk_points = 0
        
        if recent_24h >= 3:
            is_suspicious = True
            risk_points += 25
        elif recent_7d >= 10:
            is_suspicious = True
            risk_points += 20
        elif recent_30d >= 20:
            is_suspicious = True
            risk_points += 15
        
        return {
            "is_suspicious": is_suspicious,
            "risk_points": risk_points,
            "requests_24h": recent_24h,
            "requests_7d": recent_7d,
            "requests_30d": recent_30d
        }
    
    @staticmethod
    def _check_debt_ratio(db: Session, customer_id: str) -> Dict[str, Any]:
        """Check for high debt ratio"""
        
        # Get total active debt
        total_debt = db.query(func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0)).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).scalar()
        
        # Get number of active plans
        active_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).count()
        
        is_suspicious = False
        risk_points = 0
        
        # High debt amount
        if total_debt > 50000:
            is_suspicious = True
            risk_points += 20
        elif total_debt > 25000:
            risk_points += 10
        
        # Too many active plans
        if active_plans > 5:
            is_suspicious = True
            risk_points += 15
        elif active_plans > 3:
            risk_points += 8
        
        return {
            "is_suspicious": is_suspicious,
            "risk_points": risk_points,
            "total_debt": float(total_debt),
            "active_plans": active_plans
        }
    
    @staticmethod
    def _check_cross_business_pattern(db: Session, customer_id: str) -> Dict[str, Any]:
        """Check for cross-business installment chains"""
        
        # Get installment plans across different businesses in last 90 days
        recent_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.created_at >= datetime.utcnow() - timedelta(days=90)
        ).all()
        
        # Count unique businesses
        unique_businesses = len(set(plan.business_id for plan in recent_plans))
        
        # Check for rapid business switching
        business_switches = 0
        if len(recent_plans) > 1:
            sorted_plans = sorted(recent_plans, key=lambda x: x.created_at)
            for i in range(1, len(sorted_plans)):
                if sorted_plans[i].business_id != sorted_plans[i-1].business_id:
                    business_switches += 1
        
        is_suspicious = False
        risk_points = 0
        
        if unique_businesses >= 5 and len(recent_plans) >= 5:
            is_suspicious = True
            risk_points += 25
        elif unique_businesses >= 3 and business_switches >= 3:
            is_suspicious = True
            risk_points += 15
        
        return {
            "is_suspicious": is_suspicious,
            "risk_points": risk_points,
            "unique_businesses_90d": unique_businesses,
            "business_switches": business_switches,
            "total_plans_90d": len(recent_plans)
        }
    
    @staticmethod
    def _check_payment_defaults(db: Session, customer_id: str) -> Dict[str, Any]:
        """Check for payment default patterns"""
        
        # Get all payments for customer
        payments = db.query(Payment).join(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id
        ).all()
        
        if not payments:
            return {
                "is_suspicious": False,
                "risk_points": 0,
                "total_payments": 0,
                "overdue_payments": 0,
                "default_rate": 0.0
            }
        
        # Count overdue payments
        overdue_payments = len([p for p in payments if p.status == PaymentStatus.OVERDUE])
        
        # Count defaulted plans
        defaulted_plans = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.DEFAULTED
        ).count()
        
        default_rate = (overdue_payments / len(payments)) * 100 if payments else 0
        
        is_suspicious = False
        risk_points = 0
        
        if defaulted_plans > 0:
            is_suspicious = True
            risk_points += 30
        elif default_rate > 20:
            is_suspicious = True
            risk_points += 20
        elif default_rate > 10:
            risk_points += 10
        
        return {
            "is_suspicious": is_suspicious,
            "risk_points": risk_points,
            "total_payments": len(payments),
            "overdue_payments": overdue_payments,
            "defaulted_plans": defaulted_plans,
            "default_rate": round(default_rate, 2)
        }
    
    @staticmethod
    def _check_product_patterns(db: Session, customer_id: str) -> Dict[str, Any]:
        """Check for unusual product selection patterns"""
        
        # Get recent requests
        recent_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=90)
        ).all()
        
        if len(recent_requests) < 3:
            return {
                "is_suspicious": False,
                "risk_points": 0,
                "total_requests": len(recent_requests)
            }
        
        # Check for high-value items pattern
        high_value_items = [r for r in recent_requests if r.product_value > 10000]
        
        # Check for similar product names (potential resale pattern)
        product_names = [r.product_name.lower() for r in recent_requests]
        similar_products = len(product_names) - len(set(product_names))
        
        is_suspicious = False
        risk_points = 0
        
        if len(high_value_items) >= 3:
            is_suspicious = True
            risk_points += 15
        
        if similar_products >= 2:
            is_suspicious = True
            risk_points += 10
        
        return {
            "is_suspicious": is_suspicious,
            "risk_points": risk_points,
            "total_requests": len(recent_requests),
            "high_value_items": len(high_value_items),
            "similar_products": similar_products
        }
    
    @staticmethod
    def _generate_recommendations(risk_level: str, risk_factors: List[str]) -> List[str]:
        """Generate recommendations based on risk assessment"""
        
        recommendations = []
        
        if risk_level == "CRITICAL":
            recommendations.append("REJECT: High fraud risk detected")
            recommendations.append("Require additional verification documents")
            recommendations.append("Consider reporting to fraud prevention authorities")
        elif risk_level == "HIGH":
            recommendations.append("CAUTION: Require additional verification")
            recommendations.append("Consider lower credit limit or shorter terms")
            recommendations.append("Implement enhanced monitoring")
        elif risk_level == "MEDIUM":
            recommendations.append("REVIEW: Manual review recommended")
            recommendations.append("Consider standard verification procedures")
            recommendations.append("Monitor payment behavior closely")
        else:
            recommendations.append("APPROVE: Low risk customer")
            recommendations.append("Standard terms and conditions apply")
        
        # Add specific recommendations based on risk factors
        if "Rapid request pattern detected" in risk_factors:
            recommendations.append("Implement cooling-off period between requests")
        
        if "Cross-business installment chain" in risk_factors:
            recommendations.append("Verify legitimate business need for multiple installments")
        
        if "Payment default pattern" in risk_factors:
            recommendations.append("Require guarantor or collateral")
        
        return recommendations
    
    @staticmethod
    def create_fraud_alert(
        db: Session,
        customer_id: str,
        alert_type: AlertType,
        description: str,
        metadata: Dict[str, Any],
        severity: AlertSeverity = AlertSeverity.MEDIUM
    ) -> FraudAlert:
        """Create a new fraud alert"""
        
        # Check for duplicate alerts in last 24 hours
        existing_alert = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id,
            FraudAlert.alert_type == alert_type,
            FraudAlert.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).first()
        
        if existing_alert:
            logger.info(f"Duplicate fraud alert prevented for customer {customer_id}")
            return existing_alert
        
        # Create new alert
        fraud_alert = FraudAlert(
            customer_id=customer_id,
            alert_type=alert_type,
            description=description,
            alert_metadata=metadata,
            severity=severity,
            status=AlertStatus.ACTIVE
        )
        
        db.add(fraud_alert)
        db.commit()
        db.refresh(fraud_alert)
        
        logger.warning(f"Fraud alert created: {alert_type} for customer {customer_id}")
        return fraud_alert
    
    @staticmethod
    def update_fraud_patterns(db: Session, customer_id: str):
        """Update fraud patterns for a customer based on recent activity"""
        
        # This would typically be called after new installment activity
        risk_assessment = FraudDetectionService.calculate_customer_risk_score(db, customer_id)
        
        # Create or update fraud pattern record
        existing_pattern = db.query(FraudPattern).filter(
            FraudPattern.customer_id == customer_id,
            FraudPattern.pattern_type == "comprehensive_risk"
        ).first()
        
        if existing_pattern:
            existing_pattern.pattern_data = risk_assessment['risk_details']
            existing_pattern.risk_score = Decimal(str(risk_assessment['risk_score'] / 100))
            existing_pattern.detected_at = datetime.utcnow()
        else:
            fraud_pattern = FraudPattern(
                customer_id=customer_id,
                pattern_type="comprehensive_risk",
                pattern_data=risk_assessment['risk_details'],
                risk_score=Decimal(str(risk_assessment['risk_score'] / 100))
            )
            db.add(fraud_pattern)
        
        db.commit()
        
        # Create alerts for high-risk customers
        if risk_assessment['risk_level'] in ['HIGH', 'CRITICAL']:
            FraudDetectionService.create_fraud_alert(
                db=db,
                customer_id=customer_id,
                alert_type=AlertType.HIGH_DEBT_RATIO,  # Generic high-risk alert
                description=f"High risk customer detected: {risk_assessment['risk_level']}",
                metadata=risk_assessment,
                severity=AlertSeverity.HIGH if risk_assessment['risk_level'] == 'HIGH' else AlertSeverity.CRITICAL
            )