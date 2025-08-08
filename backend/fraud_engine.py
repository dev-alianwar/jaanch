"""
Core fraud detection engine for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import asyncio
from dataclasses import dataclass
from enum import Enum

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, AlertType, AlertSeverity, AlertStatus,
    RequestStatus, PlanStatus, PaymentStatus
)
from fraud_service import FraudDetectionService

logger = logging.getLogger(__name__)

class FraudRiskLevel(Enum):
    """Fraud risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FraudDetectionResult:
    """Result of fraud detection analysis"""
    customer_id: str
    risk_level: FraudRiskLevel
    risk_score: float
    detected_patterns: List[str]
    recommendations: List[str]
    should_block: bool
    requires_manual_review: bool
    confidence_score: float

class FraudDetectionEngine:
    """Core fraud detection engine with advanced pattern recognition"""
    
    def __init__(self, db: Session):
        self.db = db
        self.detection_rules = self._initialize_detection_rules()
        self.thresholds = self._load_detection_thresholds()
    
    def analyze_customer(self, customer_id: str) -> FraudDetectionResult:
        """Perform comprehensive fraud analysis on a customer"""
        
        logger.info(f"Starting fraud analysis for customer {customer_id}")
        
        # Run all detection algorithms
        rapid_requests = self._detect_rapid_requests(customer_id)
        debt_ratio = self._detect_high_debt_ratio(customer_id)
        cross_business = self._detect_cross_business_chains(customer_id)
        payment_defaults = self._detect_payment_default_patterns(customer_id)
        velocity_patterns = self._detect_velocity_patterns(customer_id)
        product_patterns = self._detect_product_patterns(customer_id)
        behavioral_anomalies = self._detect_behavioral_anomalies(customer_id)
        
        # Aggregate results
        all_patterns = [
            rapid_requests, debt_ratio, cross_business, payment_defaults,
            velocity_patterns, product_patterns, behavioral_anomalies
        ]
        
        # Calculate overall risk score
        total_risk_score = sum(pattern.risk_score for pattern in all_patterns)
        detected_patterns = [pattern.pattern_name for pattern in all_patterns if pattern.is_detected]
        
        # Determine risk level
        risk_level = self._calculate_risk_level(total_risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_level, detected_patterns, all_patterns)
        
        # Determine actions
        should_block = risk_level == FraudRiskLevel.CRITICAL
        requires_manual_review = risk_level in [FraudRiskLevel.HIGH, FraudRiskLevel.CRITICAL]
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(all_patterns)
        
        result = FraudDetectionResult(
            customer_id=customer_id,
            risk_level=risk_level,
            risk_score=min(total_risk_score, 100.0),
            detected_patterns=detected_patterns,
            recommendations=recommendations,
            should_block=should_block,
            requires_manual_review=requires_manual_review,
            confidence_score=confidence_score
        )
        
        # Store results and create alerts if necessary
        self._store_detection_results(result, all_patterns)
        
        logger.info(f"Fraud analysis completed for customer {customer_id}: {risk_level.value} risk")
        
        return result
    
    def _detect_rapid_requests(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect rapid installment request patterns"""
        
        # Get request counts for different time periods
        now = datetime.utcnow()
        
        requests_1h = self.db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= now - timedelta(hours=1)
        ).count()
        
        requests_24h = self.db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= now - timedelta(hours=24)
        ).count()
        
        requests_7d = self.db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= now - timedelta(days=7)
        ).count()
        
        # Analyze patterns
        risk_score = 0
        is_detected = False
        details = {
            "requests_1h": requests_1h,
            "requests_24h": requests_24h,
            "requests_7d": requests_7d
        }
        
        # Critical: Multiple requests in 1 hour
        if requests_1h >= 3:
            risk_score += 40
            is_detected = True
            details["trigger"] = "multiple_requests_1h"
        
        # High: Too many requests in 24 hours
        elif requests_24h >= 5:
            risk_score += 30
            is_detected = True
            details["trigger"] = "excessive_requests_24h"
        
        # Medium: High frequency over 7 days
        elif requests_7d >= 15:
            risk_score += 20
            is_detected = True
            details["trigger"] = "high_frequency_7d"
        
        return PatternDetectionResult(
            pattern_name="rapid_requests",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.9 if is_detected else 0.1,
            details=details,
            description="Customer making requests at unusually high frequency"
        )
    
    def _detect_high_debt_ratio(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect high debt ratio patterns"""
        
        # Get total active debt
        total_debt = self.db.query(func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0)).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).scalar()
        
        # Get number of active plans
        active_plans = self.db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).count()
        
        # Get unique businesses
        unique_businesses = self.db.query(func.count(func.distinct(InstallmentPlan.business_id))).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.ACTIVE
        ).scalar()
        
        risk_score = 0
        is_detected = False
        details = {
            "total_debt": float(total_debt),
            "active_plans": active_plans,
            "unique_businesses": unique_businesses
        }
        
        # Critical: Very high debt
        if total_debt > 100000:
            risk_score += 35
            is_detected = True
            details["trigger"] = "very_high_debt"
        
        # High: High debt
        elif total_debt > 50000:
            risk_score += 25
            is_detected = True
            details["trigger"] = "high_debt"
        
        # Medium: Moderate debt with many plans
        elif total_debt > 25000 and active_plans > 5:
            risk_score += 15
            is_detected = True
            details["trigger"] = "moderate_debt_many_plans"
        
        # Additional risk for too many active plans
        if active_plans > 7:
            risk_score += 15
            is_detected = True
            details["additional_risk"] = "too_many_active_plans"
        
        # Additional risk for too many businesses
        if unique_businesses > 5:
            risk_score += 10
            is_detected = True
            details["additional_risk"] = "too_many_businesses"
        
        return PatternDetectionResult(
            pattern_name="high_debt_ratio",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.8 if is_detected else 0.2,
            details=details,
            description="Customer has unusually high debt exposure"
        )
    
    def _detect_cross_business_chains(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect cross-business installment chains"""
        
        # Get recent installment plans (last 90 days)
        recent_plans = self.db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.created_at >= datetime.utcnow() - timedelta(days=90)
        ).order_by(InstallmentPlan.created_at).all()
        
        if len(recent_plans) < 3:
            return PatternDetectionResult(
                pattern_name="cross_business_chains",
                is_detected=False,
                risk_score=0,
                confidence=0.1,
                details={"recent_plans": len(recent_plans)},
                description="Insufficient data for cross-business analysis"
            )
        
        # Analyze business switching patterns
        business_switches = 0
        rapid_switches = 0
        business_sequence = []
        
        for i, plan in enumerate(recent_plans):
            business_sequence.append({
                "business_id": str(plan.business_id),
                "date": plan.created_at.isoformat(),
                "amount": float(plan.total_amount)
            })
            
            if i > 0 and plan.business_id != recent_plans[i-1].business_id:
                business_switches += 1
                
                # Check for rapid switches (within 14 days)
                time_diff = plan.created_at - recent_plans[i-1].created_at
                if time_diff.days <= 14:
                    rapid_switches += 1
        
        unique_businesses = len(set(plan.business_id for plan in recent_plans))
        
        risk_score = 0
        is_detected = False
        details = {
            "recent_plans": len(recent_plans),
            "unique_businesses": unique_businesses,
            "business_switches": business_switches,
            "rapid_switches": rapid_switches,
            "business_sequence": business_sequence
        }
        
        # Critical: Many rapid switches
        if rapid_switches >= 3:
            risk_score += 35
            is_detected = True
            details["trigger"] = "many_rapid_switches"
        
        # High: Frequent business switching
        elif business_switches >= 5 and unique_businesses >= 4:
            risk_score += 25
            is_detected = True
            details["trigger"] = "frequent_switching"
        
        # Medium: Moderate switching pattern
        elif business_switches >= 3 and unique_businesses >= 3:
            risk_score += 15
            is_detected = True
            details["trigger"] = "moderate_switching"
        
        return PatternDetectionResult(
            pattern_name="cross_business_chains",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.85 if is_detected else 0.15,
            details=details,
            description="Customer showing cross-business installment chain patterns"
        )
    
    def _detect_payment_default_patterns(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect payment default patterns"""
        
        # Get all payments for customer
        payments = self.db.query(Payment).join(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id
        ).all()
        
        if not payments:
            return PatternDetectionResult(
                pattern_name="payment_default_patterns",
                is_detected=False,
                risk_score=0,
                confidence=0.1,
                details={"total_payments": 0},
                description="No payment history available"
            )
        
        # Analyze payment patterns
        total_payments = len(payments)
        overdue_payments = len([p for p in payments if p.status == PaymentStatus.OVERDUE])
        late_payments = len([p for p in payments if p.status == PaymentStatus.PAID and p.paid_date and p.paid_date > p.due_date])
        
        # Get defaulted plans
        defaulted_plans = self.db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id,
            InstallmentPlan.status == PlanStatus.DEFAULTED
        ).count()
        
        # Calculate rates
        overdue_rate = (overdue_payments / total_payments) * 100 if total_payments > 0 else 0
        late_rate = (late_payments / total_payments) * 100 if total_payments > 0 else 0
        
        risk_score = 0
        is_detected = False
        details = {
            "total_payments": total_payments,
            "overdue_payments": overdue_payments,
            "late_payments": late_payments,
            "defaulted_plans": defaulted_plans,
            "overdue_rate": round(overdue_rate, 2),
            "late_rate": round(late_rate, 2)
        }
        
        # Critical: Has defaulted plans
        if defaulted_plans > 0:
            risk_score += 40
            is_detected = True
            details["trigger"] = "has_defaulted_plans"
        
        # High: High overdue rate
        elif overdue_rate > 30:
            risk_score += 30
            is_detected = True
            details["trigger"] = "high_overdue_rate"
        
        # Medium: Moderate payment issues
        elif overdue_rate > 15 or late_rate > 40:
            risk_score += 20
            is_detected = True
            details["trigger"] = "moderate_payment_issues"
        
        return PatternDetectionResult(
            pattern_name="payment_default_patterns",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.9 if is_detected else 0.1,
            details=details,
            description="Customer showing payment reliability issues"
        )
    
    def _detect_velocity_patterns(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect unusual velocity patterns in installment activity"""
        
        # Get installment requests over time
        requests_by_month = self.db.query(
            func.date_trunc('month', InstallmentRequest.created_at).label('month'),
            func.count(InstallmentRequest.id).label('count'),
            func.sum(InstallmentRequest.product_value).label('total_value')
        ).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=180)
        ).group_by(func.date_trunc('month', InstallmentRequest.created_at)).all()
        
        if len(requests_by_month) < 2:
            return PatternDetectionResult(
                pattern_name="velocity_patterns",
                is_detected=False,
                risk_score=0,
                confidence=0.1,
                details={"months_data": len(requests_by_month)},
                description="Insufficient data for velocity analysis"
            )
        
        # Analyze velocity changes
        monthly_counts = [month.count for month in requests_by_month]
        monthly_values = [float(month.total_value) for month in requests_by_month]
        
        # Calculate velocity metrics
        max_monthly_requests = max(monthly_counts)
        avg_monthly_requests = sum(monthly_counts) / len(monthly_counts)
        max_monthly_value = max(monthly_values)
        avg_monthly_value = sum(monthly_values) / len(monthly_values)
        
        risk_score = 0
        is_detected = False
        details = {
            "months_analyzed": len(requests_by_month),
            "max_monthly_requests": max_monthly_requests,
            "avg_monthly_requests": round(avg_monthly_requests, 2),
            "max_monthly_value": max_monthly_value,
            "avg_monthly_value": round(avg_monthly_value, 2)
        }
        
        # Detect sudden spikes
        if max_monthly_requests > avg_monthly_requests * 3 and max_monthly_requests > 5:
            risk_score += 20
            is_detected = True
            details["trigger"] = "request_count_spike"
        
        if max_monthly_value > avg_monthly_value * 4 and max_monthly_value > 20000:
            risk_score += 15
            is_detected = True
            details["trigger"] = "value_spike"
        
        return PatternDetectionResult(
            pattern_name="velocity_patterns",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.7 if is_detected else 0.3,
            details=details,
            description="Customer showing unusual velocity patterns"
        )
    
    def _detect_product_patterns(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect unusual product selection patterns"""
        
        # Get recent requests
        recent_requests = self.db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=90)
        ).all()
        
        if len(recent_requests) < 3:
            return PatternDetectionResult(
                pattern_name="product_patterns",
                is_detected=False,
                risk_score=0,
                confidence=0.1,
                details={"recent_requests": len(recent_requests)},
                description="Insufficient data for product pattern analysis"
            )
        
        # Analyze product patterns
        product_names = [req.product_name.lower() for req in recent_requests]
        product_values = [float(req.product_value) for req in recent_requests]
        
        # Check for high-value items
        high_value_items = [v for v in product_values if v > 10000]
        
        # Check for similar product names (potential resale)
        unique_products = len(set(product_names))
        similar_products = len(product_names) - unique_products
        
        # Check for luxury/resale-prone categories
        luxury_keywords = ['iphone', 'macbook', 'laptop', 'jewelry', 'watch', 'gold', 'diamond']
        luxury_items = sum(1 for name in product_names if any(keyword in name for keyword in luxury_keywords))
        
        risk_score = 0
        is_detected = False
        details = {
            "recent_requests": len(recent_requests),
            "high_value_items": len(high_value_items),
            "similar_products": similar_products,
            "luxury_items": luxury_items,
            "avg_product_value": round(sum(product_values) / len(product_values), 2)
        }
        
        # High: Many high-value items
        if len(high_value_items) >= 3:
            risk_score += 20
            is_detected = True
            details["trigger"] = "many_high_value_items"
        
        # Medium: Similar products (potential resale)
        if similar_products >= 2:
            risk_score += 15
            is_detected = True
            details["trigger"] = "similar_products"
        
        # Medium: Many luxury items
        if luxury_items >= 3:
            risk_score += 12
            is_detected = True
            details["trigger"] = "many_luxury_items"
        
        return PatternDetectionResult(
            pattern_name="product_patterns",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.6 if is_detected else 0.4,
            details=details,
            description="Customer showing unusual product selection patterns"
        )
    
    def _detect_behavioral_anomalies(self, customer_id: str) -> 'PatternDetectionResult':
        """Detect behavioral anomalies and inconsistencies"""
        
        # Get customer's complete activity
        requests = self.db.query(InstallmentRequest).filter(
            InstallmentRequest.customer_id == customer_id
        ).order_by(InstallmentRequest.created_at).all()
        
        if len(requests) < 5:
            return PatternDetectionResult(
                pattern_name="behavioral_anomalies",
                is_detected=False,
                risk_score=0,
                confidence=0.1,
                details={"total_requests": len(requests)},
                description="Insufficient data for behavioral analysis"
            )
        
        # Analyze behavioral patterns
        request_times = [req.created_at for req in requests]
        request_amounts = [float(req.product_value) for req in requests]
        
        # Check for unusual timing patterns
        time_gaps = []
        for i in range(1, len(request_times)):
            gap = (request_times[i] - request_times[i-1]).total_seconds() / 3600  # hours
            time_gaps.append(gap)
        
        # Check for very short gaps (automated behavior)
        very_short_gaps = [gap for gap in time_gaps if gap < 1]  # Less than 1 hour
        
        # Check for amount patterns
        amount_variance = max(request_amounts) - min(request_amounts) if request_amounts else 0
        
        risk_score = 0
        is_detected = False
        details = {
            "total_requests": len(requests),
            "very_short_gaps": len(very_short_gaps),
            "amount_variance": amount_variance,
            "avg_gap_hours": round(sum(time_gaps) / len(time_gaps), 2) if time_gaps else 0
        }
        
        # Detect automated/bot-like behavior
        if len(very_short_gaps) >= 3:
            risk_score += 25
            is_detected = True
            details["trigger"] = "automated_behavior"
        
        # Detect unusual amount patterns
        if amount_variance > 50000:
            risk_score += 10
            is_detected = True
            details["trigger"] = "high_amount_variance"
        
        return PatternDetectionResult(
            pattern_name="behavioral_anomalies",
            is_detected=is_detected,
            risk_score=risk_score,
            confidence=0.7 if is_detected else 0.3,
            details=details,
            description="Customer showing behavioral anomalies"
        )
    
    def _calculate_risk_level(self, total_risk_score: float) -> FraudRiskLevel:
        """Calculate overall risk level based on total risk score"""
        
        if total_risk_score >= 80:
            return FraudRiskLevel.CRITICAL
        elif total_risk_score >= 60:
            return FraudRiskLevel.HIGH
        elif total_risk_score >= 30:
            return FraudRiskLevel.MEDIUM
        else:
            return FraudRiskLevel.LOW
    
    def _generate_recommendations(
        self,
        risk_level: FraudRiskLevel,
        detected_patterns: List[str],
        all_patterns: List['PatternDetectionResult']
    ) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        
        recommendations = []
        
        # Base recommendations by risk level
        if risk_level == FraudRiskLevel.CRITICAL:
            recommendations.extend([
                "BLOCK: Immediate rejection recommended",
                "Report to fraud investigation team",
                "Flag customer account for enhanced monitoring"
            ])
        elif risk_level == FraudRiskLevel.HIGH:
            recommendations.extend([
                "MANUAL REVIEW: Require human approval",
                "Request additional verification documents",
                "Consider reduced credit limits"
            ])
        elif risk_level == FraudRiskLevel.MEDIUM:
            recommendations.extend([
                "CAUTION: Enhanced verification recommended",
                "Monitor payment behavior closely",
                "Consider shorter installment terms"
            ])
        else:
            recommendations.append("APPROVE: Low risk customer")
        
        # Pattern-specific recommendations
        if "rapid_requests" in detected_patterns:
            recommendations.append("Implement cooling-off period between requests")
        
        if "cross_business_chains" in detected_patterns:
            recommendations.append("Verify legitimate business need across multiple vendors")
        
        if "payment_default_patterns" in detected_patterns:
            recommendations.append("Require guarantor or additional collateral")
        
        if "high_debt_ratio" in detected_patterns:
            recommendations.append("Assess total debt capacity before approval")
        
        return recommendations
    
    def _calculate_confidence_score(self, patterns: List['PatternDetectionResult']) -> float:
        """Calculate confidence score for the overall analysis"""
        
        if not patterns:
            return 0.0
        
        # Weight confidence by risk score
        total_weighted_confidence = sum(p.confidence * p.risk_score for p in patterns)
        total_risk_score = sum(p.risk_score for p in patterns)
        
        if total_risk_score == 0:
            return 0.5  # Neutral confidence when no risk detected
        
        return min(total_weighted_confidence / total_risk_score, 1.0)
    
    def _store_detection_results(
        self,
        result: FraudDetectionResult,
        patterns: List['PatternDetectionResult']
    ):
        """Store fraud detection results and create alerts if necessary"""
        
        # Create fraud pattern record
        pattern_data = {
            "risk_level": result.risk_level.value,
            "risk_score": result.risk_score,
            "detected_patterns": result.detected_patterns,
            "confidence_score": result.confidence_score,
            "pattern_details": {p.pattern_name: p.details for p in patterns if p.is_detected}
        }
        
        fraud_pattern = FraudPattern(
            customer_id=result.customer_id,
            pattern_type="comprehensive_analysis",
            pattern_data=pattern_data,
            risk_score=Decimal(str(result.risk_score / 100))
        )
        
        self.db.add(fraud_pattern)
        
        # Create fraud alert if high risk
        if result.risk_level in [FraudRiskLevel.HIGH, FraudRiskLevel.CRITICAL]:
            alert_severity = AlertSeverity.HIGH if result.risk_level == FraudRiskLevel.HIGH else AlertSeverity.CRITICAL
            
            fraud_alert = FraudAlert(
                customer_id=result.customer_id,
                alert_type=AlertType.CROSS_BUSINESS_CHAIN,  # Generic high-risk alert
                description=f"High fraud risk detected: {result.risk_level.value.upper()}",
                alert_metadata=pattern_data,
                severity=alert_severity,
                status=AlertStatus.ACTIVE
            )
            
            self.db.add(fraud_alert)
        
        self.db.commit()
    
    def _initialize_detection_rules(self) -> Dict[str, Any]:
        """Initialize fraud detection rules and weights"""
        
        return {
            "rapid_requests": {
                "weight": 1.0,
                "thresholds": {
                    "critical_1h": 3,
                    "high_24h": 5,
                    "medium_7d": 15
                }
            },
            "debt_ratio": {
                "weight": 1.2,
                "thresholds": {
                    "critical_debt": 100000,
                    "high_debt": 50000,
                    "medium_debt": 25000,
                    "max_active_plans": 7,
                    "max_businesses": 5
                }
            },
            "cross_business": {
                "weight": 1.5,
                "thresholds": {
                    "critical_rapid_switches": 3,
                    "high_switches": 5,
                    "medium_switches": 3,
                    "rapid_switch_days": 14
                }
            },
            "payment_defaults": {
                "weight": 1.3,
                "thresholds": {
                    "critical_overdue_rate": 30,
                    "medium_overdue_rate": 15,
                    "high_late_rate": 40
                }
            }
        }
    
    def _load_detection_thresholds(self) -> Dict[str, Any]:
        """Load configurable detection thresholds"""
        
        # In production, these would be loaded from configuration
        return {
            "max_active_debt": 100000,
            "max_active_plans": 7,
            "max_businesses": 5,
            "rapid_request_hours": 24,
            "rapid_switch_days": 14,
            "high_value_threshold": 10000,
            "critical_risk_threshold": 80,
            "high_risk_threshold": 60,
            "medium_risk_threshold": 30
        }

@dataclass
class PatternDetectionResult:
    """Result of individual pattern detection"""
    pattern_name: str
    is_detected: bool
    risk_score: float
    confidence: float
    details: Dict[str, Any]
    description: str