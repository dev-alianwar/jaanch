"""
Admin dashboard service layer for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, text
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import logging

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, UserRole, RequestStatus, PlanStatus,
    PaymentStatus, AlertType, AlertSeverity, AlertStatus
)

logger = logging.getLogger(__name__)

class AdminDashboardService:
    """Service class for admin dashboard operations"""
    
    @staticmethod
    def get_system_overview(db: Session) -> Dict[str, Any]:
        """Get comprehensive system overview"""
        
        # User statistics
        user_stats = db.query(
            User.role,
            func.count(User.id).label('count'),
            func.count(func.nullif(User.is_active, False)).label('active_count')
        ).group_by(User.role).all()
        
        # Business statistics
        business_stats = db.query(
            func.count(Business.id).label('total'),
            func.count(func.nullif(Business.is_verified, False)).label('verified')
        ).first()
        
        # Request statistics
        request_stats = db.query(
            func.count(InstallmentRequest.id).label('total'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.PENDING, True)).label('pending'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.REJECTED, True)).label('rejected')
        ).first()
        
        # Plan statistics
        plan_stats = db.query(
            func.count(InstallmentPlan.id).label('total'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.ACTIVE, True)).label('active'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_value'),
            func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0).label('outstanding')
        ).first()
        
        # Fraud statistics
        fraud_stats = db.query(
            func.count(FraudAlert.id).label('total_alerts'),
            func.count(func.nullif(FraudAlert.status != AlertStatus.ACTIVE, True)).label('active_alerts'),
            func.count(func.nullif(FraudAlert.severity != AlertSeverity.CRITICAL, True)).label('critical_alerts')
        ).first()
        
        # Format user statistics
        user_summary = {}
        total_users = 0
        active_users = 0
        
        for stat in user_stats:
            role_name = stat.role.value
            user_summary[role_name] = {
                'total': stat.count,
                'active': stat.active_count
            }
            total_users += stat.count
            active_users += stat.active_count
        
        return {
            'users': {
                'total': total_users,
                'active': active_users,
                'by_role': user_summary
            },
            'businesses': {
                'total': business_stats.total,
                'verified': business_stats.verified,
                'verification_rate': round((business_stats.verified / business_stats.total * 100) if business_stats.total > 0 else 0, 2)
            },
            'requests': {
                'total': request_stats.total,
                'pending': request_stats.pending,
                'approved': request_stats.approved,
                'rejected': request_stats.rejected,
                'approval_rate': round((request_stats.approved / request_stats.total * 100) if request_stats.total > 0 else 0, 2)
            },
            'plans': {
                'total': plan_stats.total,
                'active': plan_stats.active,
                'completed': plan_stats.completed,
                'defaulted': plan_stats.defaulted,
                'completion_rate': round((plan_stats.completed / plan_stats.total * 100) if plan_stats.total > 0 else 0, 2),
                'default_rate': round((plan_stats.defaulted / plan_stats.total * 100) if plan_stats.total > 0 else 0, 2)
            },
            'financial': {
                'total_value': float(plan_stats.total_value),
                'outstanding_amount': float(plan_stats.outstanding),
                'collection_rate': round(((float(plan_stats.total_value) - float(plan_stats.outstanding)) / float(plan_stats.total_value) * 100) if plan_stats.total_value > 0 else 0, 2)
            },
            'fraud': {
                'total_alerts': fraud_stats.total_alerts,
                'active_alerts': fraud_stats.active_alerts,
                'critical_alerts': fraud_stats.critical_alerts
            },
            'generated_at': datetime.utcnow().isoformat()
        }    

    @staticmethod
    def get_system_metrics(db: Session, days: int) -> Dict[str, Any]:
        """Get detailed system metrics for specified period"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Daily activity metrics
        daily_metrics = db.query(
            func.date(InstallmentRequest.created_at).label('date'),
            func.count(InstallmentRequest.id).label('requests'),
            func.sum(InstallmentRequest.product_value).label('request_value')
        ).filter(
            InstallmentRequest.created_at >= cutoff_date
        ).group_by(
            func.date(InstallmentRequest.created_at)
        ).order_by(
            func.date(InstallmentRequest.created_at)
        ).all()
        
        # Growth metrics
        current_period_requests = db.query(func.count(InstallmentRequest.id)).filter(
            InstallmentRequest.created_at >= cutoff_date
        ).scalar()
        
        previous_period_requests = db.query(func.count(InstallmentRequest.id)).filter(
            InstallmentRequest.created_at >= cutoff_date - timedelta(days=days),
            InstallmentRequest.created_at < cutoff_date
        ).scalar()
        
        growth_rate = 0
        if previous_period_requests > 0:
            growth_rate = ((current_period_requests - previous_period_requests) / previous_period_requests) * 100
        
        # Top businesses by volume
        top_businesses = db.query(
            Business.business_name,
            func.count(InstallmentRequest.id).label('request_count'),
            func.sum(InstallmentRequest.product_value).label('total_value')
        ).join(InstallmentRequest).filter(
            InstallmentRequest.created_at >= cutoff_date
        ).group_by(Business.id, Business.business_name).order_by(
            func.count(InstallmentRequest.id).desc()
        ).limit(10).all()
        
        return {
            'period_days': days,
            'daily_activity': [
                {
                    'date': metric.date.isoformat(),
                    'requests': metric.requests,
                    'request_value': float(metric.request_value or 0)
                }
                for metric in daily_metrics
            ],
            'growth': {
                'current_period_requests': current_period_requests,
                'previous_period_requests': previous_period_requests,
                'growth_rate': round(growth_rate, 2)
            },
            'top_businesses': [
                {
                    'name': business.business_name,
                    'request_count': business.request_count,
                    'total_value': float(business.total_value or 0)
                }
                for business in top_businesses
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_fraud_summary(db: Session) -> Dict[str, Any]:
        """Get comprehensive fraud detection summary"""
        
        # Alert statistics by severity and type
        alert_stats = db.query(
            FraudAlert.severity,
            FraudAlert.alert_type,
            FraudAlert.status,
            func.count(FraudAlert.id).label('count')
        ).group_by(
            FraudAlert.severity,
            FraudAlert.alert_type,
            FraudAlert.status
        ).all()
        
        # Recent high-risk patterns
        high_risk_patterns = db.query(FraudPattern).filter(
            FraudPattern.risk_score >= 0.7,
            FraudPattern.detected_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(FraudPattern.detected_at.desc()).limit(20).all()
        
        # Fraud detection effectiveness
        total_customers_analyzed = db.query(func.count(func.distinct(FraudPattern.customer_id))).scalar()
        high_risk_customers = db.query(func.count(func.distinct(FraudPattern.customer_id))).filter(
            FraudPattern.risk_score >= 0.7
        ).scalar()
        
        # Format alert statistics
        alert_summary = {}
        for stat in alert_stats:
            severity = stat.severity.value
            alert_type = stat.alert_type.value
            status = stat.status.value
            
            if severity not in alert_summary:
                alert_summary[severity] = {}
            if alert_type not in alert_summary[severity]:
                alert_summary[severity][alert_type] = {}
            
            alert_summary[severity][alert_type][status] = stat.count
        
        return {
            'alert_summary': alert_summary,
            'recent_high_risk_patterns': [
                {
                    'customer_id': str(pattern.customer_id),
                    'pattern_type': pattern.pattern_type,
                    'risk_score': float(pattern.risk_score),
                    'detected_at': pattern.detected_at.isoformat()
                }
                for pattern in high_risk_patterns
            ],
            'effectiveness': {
                'total_customers_analyzed': total_customers_analyzed,
                'high_risk_customers': high_risk_customers,
                'high_risk_rate': round((high_risk_customers / total_customers_analyzed * 100) if total_customers_analyzed > 0 else 0, 2)
            },
            'generated_at': datetime.utcnow().isoformat()
        }    

    @staticmethod
    def get_business_analytics(db: Session) -> Dict[str, Any]:
        """Get business participation and performance analytics"""
        
        # Business performance metrics
        business_metrics = db.query(
            Business.id,
            Business.business_name,
            Business.business_type,
            Business.is_verified,
            func.count(InstallmentRequest.id).label('total_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved_requests'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted_plans'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_revenue'),
            func.count(func.distinct(InstallmentRequest.customer_id)).label('unique_customers')
        ).outerjoin(InstallmentRequest).outerjoin(InstallmentPlan).group_by(
            Business.id, Business.business_name, Business.business_type, Business.is_verified
        ).all()
        
        # Business type distribution
        type_distribution = db.query(
            Business.business_type,
            func.count(Business.id).label('count')
        ).group_by(Business.business_type).all()
        
        # Format business metrics
        business_performance = []
        for metric in business_metrics:
            approval_rate = (metric.approved_requests / metric.total_requests * 100) if metric.total_requests > 0 else 0
            default_rate = (metric.defaulted_plans / metric.approved_requests * 100) if metric.approved_requests > 0 else 0
            
            business_performance.append({
                'business_id': str(metric.id),
                'business_name': metric.business_name,
                'business_type': metric.business_type,
                'is_verified': metric.is_verified,
                'total_requests': metric.total_requests,
                'approved_requests': metric.approved_requests,
                'approval_rate': round(approval_rate, 2),
                'default_rate': round(default_rate, 2),
                'total_revenue': float(metric.total_revenue),
                'unique_customers': metric.unique_customers
            })
        
        return {
            'business_performance': business_performance,
            'type_distribution': [
                {
                    'business_type': dist.business_type or 'Unknown',
                    'count': dist.count
                }
                for dist in type_distribution
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def analyze_cross_business_patterns(db: Session, min_businesses: int, days: int) -> Dict[str, Any]:
        """Analyze cross-business installment patterns"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Find customers with multiple business relationships
        cross_business_customers = db.query(
            InstallmentPlan.customer_id,
            func.count(func.distinct(InstallmentPlan.business_id)).label('business_count'),
            func.count(InstallmentPlan.id).label('total_plans'),
            func.sum(InstallmentPlan.total_amount).label('total_amount')
        ).filter(
            InstallmentPlan.created_at >= cutoff_date
        ).group_by(
            InstallmentPlan.customer_id
        ).having(
            func.count(func.distinct(InstallmentPlan.business_id)) >= min_businesses
        ).order_by(
            func.count(func.distinct(InstallmentPlan.business_id)).desc()
        ).all()
        
        # Analyze business switching patterns
        switching_patterns = []
        for customer in cross_business_customers[:50]:  # Limit to top 50
            customer_plans = db.query(InstallmentPlan).filter(
                InstallmentPlan.customer_id == customer.customer_id,
                InstallmentPlan.created_at >= cutoff_date
            ).order_by(InstallmentPlan.created_at).all()
            
            switches = 0
            rapid_switches = 0
            
            for i in range(1, len(customer_plans)):
                if customer_plans[i].business_id != customer_plans[i-1].business_id:
                    switches += 1
                    time_diff = customer_plans[i].created_at - customer_plans[i-1].created_at
                    if time_diff.days <= 14:
                        rapid_switches += 1
            
            switching_patterns.append({
                'customer_id': str(customer.customer_id),
                'business_count': customer.business_count,
                'total_plans': customer.total_plans,
                'total_amount': float(customer.total_amount),
                'switches': switches,
                'rapid_switches': rapid_switches,
                'risk_score': min((switches * 10 + rapid_switches * 20) / 100, 1.0)
            })
        
        return {
            'analysis_period_days': days,
            'min_businesses_threshold': min_businesses,
            'cross_business_customers_count': len(cross_business_customers),
            'switching_patterns': switching_patterns,
            'generated_at': datetime.utcnow().isoformat()
        } 
   
    @staticmethod
    def analyze_fraud_detection_effectiveness(db: Session) -> Dict[str, Any]:
        """Analyze fraud detection system effectiveness"""
        
        # Get fraud detection statistics
        total_patterns = db.query(func.count(FraudPattern.id)).scalar()
        high_risk_patterns = db.query(func.count(FraudPattern.id)).filter(
            FraudPattern.risk_score >= 0.7
        ).scalar()
        
        # Alert resolution statistics
        alert_resolution = db.query(
            FraudAlert.status,
            func.count(FraudAlert.id).label('count'),
            func.avg(
                func.extract('epoch', FraudAlert.resolved_at - FraudAlert.created_at) / 3600
            ).label('avg_resolution_hours')
        ).filter(
            FraudAlert.resolved_at.isnot(None)
        ).group_by(FraudAlert.status).all()
        
        # Pattern type effectiveness
        pattern_effectiveness = db.query(
            FraudPattern.pattern_type,
            func.count(FraudPattern.id).label('total_detections'),
            func.avg(FraudPattern.risk_score).label('avg_risk_score'),
            func.count(func.nullif(FraudPattern.risk_score < 0.5, True)).label('high_confidence')
        ).group_by(FraudPattern.pattern_type).all()
        
        return {
            'overall_statistics': {
                'total_patterns_detected': total_patterns,
                'high_risk_patterns': high_risk_patterns,
                'high_risk_rate': round((high_risk_patterns / total_patterns * 100) if total_patterns > 0 else 0, 2)
            },
            'alert_resolution': [
                {
                    'status': resolution.status.value,
                    'count': resolution.count,
                    'avg_resolution_hours': round(float(resolution.avg_resolution_hours or 0), 2)
                }
                for resolution in alert_resolution
            ],
            'pattern_effectiveness': [
                {
                    'pattern_type': pattern.pattern_type,
                    'total_detections': pattern.total_detections,
                    'avg_risk_score': round(float(pattern.avg_risk_score), 3),
                    'high_confidence_rate': round((pattern.high_confidence / pattern.total_detections * 100), 2)
                }
                for pattern in pattern_effectiveness
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_system_health(db: Session) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        
        # Database health checks
        try:
            # Test basic queries
            user_count = db.query(func.count(User.id)).scalar()
            business_count = db.query(func.count(Business.id)).scalar()
            request_count = db.query(func.count(InstallmentRequest.id)).scalar()
            
            db_health = "healthy"
        except Exception as e:
            db_health = f"error: {str(e)}"
            user_count = business_count = request_count = 0
        
        # Recent activity check
        recent_activity = db.query(func.count(InstallmentRequest.id)).filter(
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar()
        
        # Fraud detection health
        recent_patterns = db.query(func.count(FraudPattern.id)).filter(
            FraudPattern.detected_at >= datetime.utcnow() - timedelta(hours=24)
        ).scalar()
        
        active_alerts = db.query(func.count(FraudAlert.id)).filter(
            FraudAlert.status == AlertStatus.ACTIVE
        ).scalar()
        
        return {
            'database': {
                'status': db_health,
                'user_count': user_count,
                'business_count': business_count,
                'request_count': request_count
            },
            'activity': {
                'recent_requests_24h': recent_activity,
                'recent_patterns_24h': recent_patterns,
                'active_alerts': active_alerts
            },
            'system_status': 'healthy' if db_health == 'healthy' else 'degraded',
            'checked_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_system_configuration(db: Session) -> Dict[str, Any]:
        """Get current system configuration and thresholds"""
        
        # This would typically be stored in a configuration table
        # For now, return default configuration
        return {
            'fraud_detection': {
                'rapid_request_threshold_1h': 3,
                'rapid_request_threshold_24h': 5,
                'rapid_request_threshold_7d': 15,
                'high_debt_threshold': 50000,
                'critical_debt_threshold': 100000,
                'max_active_plans': 7,
                'max_businesses': 5,
                'rapid_switch_days': 14,
                'high_value_threshold': 10000
            },
            'system_limits': {
                'max_installment_months': 60,
                'min_monthly_payment': 10,
                'max_product_value': 1000000
            },
            'alert_thresholds': {
                'critical_risk_score': 0.8,
                'high_risk_score': 0.6,
                'medium_risk_score': 0.3
            },
            'last_updated': datetime.utcnow().isoformat()
        }   
 
    @staticmethod
    def update_system_configuration(
        db: Session, 
        config_updates: Dict[str, Any], 
        updated_by: str
    ) -> Dict[str, Any]:
        """Update system configuration and thresholds"""
        
        # Validate configuration updates
        valid_keys = {
            'fraud_detection.rapid_request_threshold_1h',
            'fraud_detection.rapid_request_threshold_24h',
            'fraud_detection.rapid_request_threshold_7d',
            'fraud_detection.high_debt_threshold',
            'fraud_detection.critical_debt_threshold',
            'fraud_detection.max_active_plans',
            'fraud_detection.max_businesses',
            'system_limits.max_installment_months',
            'system_limits.min_monthly_payment',
            'alert_thresholds.critical_risk_score'
        }
        
        # In a real implementation, this would update a configuration table
        # For now, we'll just validate and return the updates
        
        validated_updates = {}
        for key, value in config_updates.items():
            if key in valid_keys:
                # Validate value types and ranges
                if 'threshold' in key and isinstance(value, (int, float)) and value > 0:
                    validated_updates[key] = value
                elif 'max_' in key and isinstance(value, int) and value > 0:
                    validated_updates[key] = value
                elif 'risk_score' in key and isinstance(value, (int, float)) and 0 <= value <= 1:
                    validated_updates[key] = value
                else:
                    raise ValueError(f"Invalid value for {key}: {value}")
            else:
                raise ValueError(f"Invalid configuration key: {key}")
        
        # Log configuration changes
        logger.info(f"System configuration updated by {updated_by}: {validated_updates}")
        
        return validated_updates
    
    @staticmethod
    def get_critical_alerts(db: Session, limit: int) -> Dict[str, Any]:
        """Get critical fraud alerts requiring immediate attention"""
        
        critical_alerts = db.query(FraudAlert).filter(
            FraudAlert.severity == AlertSeverity.CRITICAL,
            FraudAlert.status == AlertStatus.ACTIVE
        ).order_by(FraudAlert.created_at.desc()).limit(limit).all()
        
        # Get customer details for each alert
        alert_details = []
        for alert in critical_alerts:
            customer = db.query(User).filter(User.id == alert.customer_id).first()
            
            # Get recent activity for context
            recent_requests = db.query(func.count(InstallmentRequest.id)).filter(
                InstallmentRequest.customer_id == alert.customer_id,
                InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=7)
            ).scalar()
            
            active_debt = db.query(func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0)).filter(
                InstallmentPlan.customer_id == alert.customer_id,
                InstallmentPlan.status == PlanStatus.ACTIVE
            ).scalar()
            
            alert_details.append({
                'alert_id': str(alert.id),
                'customer_id': str(alert.customer_id),
                'customer_name': f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                'customer_email': customer.email if customer else "Unknown",
                'alert_type': alert.alert_type.value,
                'description': alert.description,
                'created_at': alert.created_at.isoformat(),
                'metadata': alert.alert_metadata,
                'context': {
                    'recent_requests_7d': recent_requests,
                    'active_debt': float(active_debt)
                }
            })
        
        return {
            'critical_alerts': alert_details,
            'total_count': len(alert_details),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def get_real_time_monitoring(db: Session) -> Dict[str, Any]:
        """Get real-time system monitoring data"""
        
        now = datetime.utcnow()
        
        # Last hour activity
        last_hour_requests = db.query(func.count(InstallmentRequest.id)).filter(
            InstallmentRequest.created_at >= now - timedelta(hours=1)
        ).scalar()
        
        last_hour_alerts = db.query(func.count(FraudAlert.id)).filter(
            FraudAlert.created_at >= now - timedelta(hours=1)
        ).scalar()
        
        # Current active sessions (approximated by recent activity)
        active_sessions = db.query(func.count(func.distinct(InstallmentRequest.customer_id))).filter(
            InstallmentRequest.created_at >= now - timedelta(minutes=30)
        ).scalar()
        
        # System load indicators
        pending_requests = db.query(func.count(InstallmentRequest.id)).filter(
            InstallmentRequest.status == RequestStatus.PENDING
        ).scalar()
        
        unresolved_alerts = db.query(func.count(FraudAlert.id)).filter(
            FraudAlert.status == AlertStatus.ACTIVE
        ).scalar()
        
        return {
            'timestamp': now.isoformat(),
            'activity': {
                'requests_last_hour': last_hour_requests,
                'alerts_last_hour': last_hour_alerts,
                'estimated_active_sessions': active_sessions
            },
            'system_load': {
                'pending_requests': pending_requests,
                'unresolved_alerts': unresolved_alerts
            },
            'status': 'operational'
        }