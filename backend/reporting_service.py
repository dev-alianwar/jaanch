"""
Reporting service for the Installment Fraud Detection System
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, text
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import json
import csv
from io import StringIO

from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, UserRole, RequestStatus, PlanStatus,
    PaymentStatus, AlertType, AlertSeverity, AlertStatus
)

logger = logging.getLogger(__name__)

class ReportingService:
    """Service class for generating comprehensive reports"""
    
    @staticmethod
    def generate_fraud_trends_report(
        db: Session, 
        days: int, 
        granularity: str
    ) -> Dict[str, Any]:
        """Generate fraud trends report with specified granularity"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Determine date truncation based on granularity
        if granularity == "daily":
            date_trunc = func.date(FraudAlert.created_at)
        elif granularity == "weekly":
            date_trunc = func.date_trunc('week', FraudAlert.created_at)
        else:  # monthly
            date_trunc = func.date_trunc('month', FraudAlert.created_at)
        
        # Get fraud alert trends
        alert_trends = db.query(
            date_trunc.label('period'),
            FraudAlert.severity,
            FraudAlert.alert_type,
            func.count(FraudAlert.id).label('count')
        ).filter(
            FraudAlert.created_at >= cutoff_date
        ).group_by(
            date_trunc,
            FraudAlert.severity,
            FraudAlert.alert_type
        ).order_by(date_trunc).all()
        
        # Get pattern detection trends
        pattern_trends = db.query(
            date_trunc.label('period'),
            FraudPattern.pattern_type,
            func.count(FraudPattern.id).label('count'),
            func.avg(FraudPattern.risk_score).label('avg_risk_score')
        ).filter(
            FraudPattern.detected_at >= cutoff_date
        ).group_by(
            date_trunc,
            FraudPattern.pattern_type
        ).order_by(date_trunc).all()
        
        # Format trends data
        trends_by_period = {}
        
        for trend in alert_trends:
            period_key = trend.period.isoformat() if hasattr(trend.period, 'isoformat') else str(trend.period)
            if period_key not in trends_by_period:
                trends_by_period[period_key] = {'alerts': {}, 'patterns': {}}
            
            severity = trend.severity.value
            alert_type = trend.alert_type.value
            
            if severity not in trends_by_period[period_key]['alerts']:
                trends_by_period[period_key]['alerts'][severity] = {}
            
            trends_by_period[period_key]['alerts'][severity][alert_type] = trend.count
        
        for trend in pattern_trends:
            period_key = trend.period.isoformat() if hasattr(trend.period, 'isoformat') else str(trend.period)
            if period_key not in trends_by_period:
                trends_by_period[period_key] = {'alerts': {}, 'patterns': {}}
            
            trends_by_period[period_key]['patterns'][trend.pattern_type] = {
                'count': trend.count,
                'avg_risk_score': round(float(trend.avg_risk_score), 3)
            }
        
        return {
            'report_type': 'fraud_trends',
            'period_days': days,
            'granularity': granularity,
            'trends_by_period': trends_by_period,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_business_performance_report(
        db: Session,
        days: int,
        sort_by: str,
        limit: int
    ) -> Dict[str, Any]:
        """Generate business performance report"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get business performance metrics
        business_performance = db.query(
            Business.id,
            Business.business_name,
            Business.business_type,
            Business.is_verified,
            Business.created_at,
            func.count(InstallmentRequest.id).label('total_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.REJECTED, True)).label('rejected_requests'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted_plans'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_revenue'),
            func.coalesce(func.sum(InstallmentPlan.paid_amount), 0).label('collected_amount'),
            func.count(func.distinct(InstallmentRequest.customer_id)).label('unique_customers')
        ).outerjoin(
            InstallmentRequest,
            and_(
                InstallmentRequest.business_id == Business.id,
                InstallmentRequest.created_at >= cutoff_date
            )
        ).outerjoin(
            InstallmentPlan,
            and_(
                InstallmentPlan.business_id == Business.id,
                InstallmentPlan.created_at >= cutoff_date
            )
        ).group_by(
            Business.id,
            Business.business_name,
            Business.business_type,
            Business.is_verified,
            Business.created_at
        ).all()
        
        # Calculate derived metrics and format results
        performance_data = []
        for perf in business_performance:
            approval_rate = (perf.approved_requests / perf.total_requests * 100) if perf.total_requests > 0 else 0
            rejection_rate = (perf.rejected_requests / perf.total_requests * 100) if perf.total_requests > 0 else 0
            default_rate = (perf.defaulted_plans / perf.approved_requests * 100) if perf.approved_requests > 0 else 0
            collection_rate = (float(perf.collected_amount) / float(perf.total_revenue) * 100) if perf.total_revenue > 0 else 0
            
            performance_data.append({
                'business_id': str(perf.id),
                'business_name': perf.business_name,
                'business_type': perf.business_type,
                'is_verified': perf.is_verified,
                'created_at': perf.created_at.isoformat(),
                'total_requests': perf.total_requests,
                'approved_requests': perf.approved_requests,
                'rejected_requests': perf.rejected_requests,
                'approval_rate': round(approval_rate, 2),
                'rejection_rate': round(rejection_rate, 2),
                'completed_plans': perf.completed_plans,
                'defaulted_plans': perf.defaulted_plans,
                'default_rate': round(default_rate, 2),
                'total_revenue': float(perf.total_revenue),
                'collected_amount': float(perf.collected_amount),
                'collection_rate': round(collection_rate, 2),
                'unique_customers': perf.unique_customers
            })
        
        # Sort by specified metric
        sort_key_map = {
            'total_revenue': lambda x: x['total_revenue'],
            'approval_rate': lambda x: x['approval_rate'],
            'default_rate': lambda x: x['default_rate'],
            'customer_count': lambda x: x['unique_customers']
        }
        
        if sort_by in sort_key_map:
            performance_data.sort(key=sort_key_map[sort_by], reverse=True)
        
        return {
            'report_type': 'business_performance',
            'period_days': days,
            'sort_by': sort_by,
            'business_performance': performance_data[:limit],
            'total_businesses': len(performance_data),
            'generated_at': datetime.utcnow().isoformat()
        }    
   
 @staticmethod
    def generate_customer_risk_analysis_report(
        db: Session,
        risk_threshold: float,
        limit: int
    ) -> Dict[str, Any]:
        """Generate customer risk analysis report"""
        
        # Get high-risk customers
        high_risk_customers = db.query(
            FraudPattern.customer_id,
            func.max(FraudPattern.risk_score).label('max_risk_score'),
            func.count(FraudPattern.id).label('pattern_count'),
            func.max(FraudPattern.detected_at).label('last_detection')
        ).filter(
            FraudPattern.risk_score >= risk_threshold
        ).group_by(
            FraudPattern.customer_id
        ).order_by(
            func.max(FraudPattern.risk_score).desc()
        ).limit(limit).all()
        
        # Get detailed information for each high-risk customer
        risk_analysis = []
        for customer_risk in high_risk_customers:
            customer = db.query(User).filter(User.id == customer_risk.customer_id).first()
            
            # Get customer's installment activity
            active_plans = db.query(func.count(InstallmentPlan.id)).filter(
                InstallmentPlan.customer_id == customer_risk.customer_id,
                InstallmentPlan.status == PlanStatus.ACTIVE
            ).scalar()
            
            total_debt = db.query(func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0)).filter(
                InstallmentPlan.customer_id == customer_risk.customer_id,
                InstallmentPlan.status == PlanStatus.ACTIVE
            ).scalar()
            
            # Get recent alerts
            recent_alerts = db.query(func.count(FraudAlert.id)).filter(
                FraudAlert.customer_id == customer_risk.customer_id,
                FraudAlert.created_at >= datetime.utcnow() - timedelta(days=30)
            ).scalar()
            
            # Get business relationships
            business_count = db.query(func.count(func.distinct(InstallmentPlan.business_id))).filter(
                InstallmentPlan.customer_id == customer_risk.customer_id
            ).scalar()
            
            risk_analysis.append({
                'customer_id': str(customer_risk.customer_id),
                'customer_name': f"{customer.first_name} {customer.last_name}" if customer else "Unknown",
                'customer_email': customer.email if customer else "Unknown",
                'max_risk_score': float(customer_risk.max_risk_score),
                'pattern_count': customer_risk.pattern_count,
                'last_detection': customer_risk.last_detection.isoformat(),
                'active_plans': active_plans,
                'total_debt': float(total_debt),
                'recent_alerts_30d': recent_alerts,
                'business_relationships': business_count
            })
        
        return {
            'report_type': 'customer_risk_analysis',
            'risk_threshold': risk_threshold,
            'high_risk_customers': risk_analysis,
            'total_analyzed': len(risk_analysis),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_financial_overview_report(db: Session, days: int) -> Dict[str, Any]:
        """Generate financial overview report"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Overall financial metrics
        financial_metrics = db.query(
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_installment_value'),
            func.coalesce(func.sum(InstallmentPlan.paid_amount), 0).label('total_collected'),
            func.coalesce(func.sum(InstallmentPlan.remaining_amount), 0).label('total_outstanding'),
            func.count(InstallmentPlan.id).label('total_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.ACTIVE, True)).label('active_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted_plans')
        ).filter(
            InstallmentPlan.created_at >= cutoff_date
        ).first()
        
        # Monthly financial trends
        monthly_trends = db.query(
            func.date_trunc('month', InstallmentPlan.created_at).label('month'),
            func.sum(InstallmentPlan.total_amount).label('monthly_value'),
            func.count(InstallmentPlan.id).label('monthly_plans')
        ).filter(
            InstallmentPlan.created_at >= cutoff_date
        ).group_by(
            func.date_trunc('month', InstallmentPlan.created_at)
        ).order_by(
            func.date_trunc('month', InstallmentPlan.created_at)
        ).all()
        
        # Payment performance
        payment_performance = db.query(
            func.count(Payment.id).label('total_payments'),
            func.count(func.nullif(Payment.status != PaymentStatus.PAID, True)).label('successful_payments'),
            func.count(func.nullif(Payment.status != PaymentStatus.OVERDUE, True)).label('overdue_payments'),
            func.sum(func.case([(Payment.status == PaymentStatus.PAID, Payment.amount)], else_=0)).label('collected_amount')
        ).join(InstallmentPlan).filter(
            InstallmentPlan.created_at >= cutoff_date
        ).first()
        
        # Calculate derived metrics
        collection_rate = (float(financial_metrics.total_collected) / float(financial_metrics.total_installment_value) * 100) if financial_metrics.total_installment_value > 0 else 0
        default_rate = (financial_metrics.defaulted_plans / financial_metrics.total_plans * 100) if financial_metrics.total_plans > 0 else 0
        payment_success_rate = (payment_performance.successful_payments / payment_performance.total_payments * 100) if payment_performance.total_payments > 0 else 0
        
        return {
            'report_type': 'financial_overview',
            'period_days': days,
            'overall_metrics': {
                'total_installment_value': float(financial_metrics.total_installment_value),
                'total_collected': float(financial_metrics.total_collected),
                'total_outstanding': float(financial_metrics.total_outstanding),
                'collection_rate': round(collection_rate, 2),
                'total_plans': financial_metrics.total_plans,
                'active_plans': financial_metrics.active_plans,
                'completed_plans': financial_metrics.completed_plans,
                'defaulted_plans': financial_metrics.defaulted_plans,
                'default_rate': round(default_rate, 2)
            },
            'monthly_trends': [
                {
                    'month': trend.month.isoformat() if hasattr(trend.month, 'isoformat') else str(trend.month),
                    'monthly_value': float(trend.monthly_value or 0),
                    'monthly_plans': trend.monthly_plans
                }
                for trend in monthly_trends
            ],
            'payment_performance': {
                'total_payments': payment_performance.total_payments,
                'successful_payments': payment_performance.successful_payments,
                'overdue_payments': payment_performance.overdue_payments,
                'payment_success_rate': round(payment_success_rate, 2),
                'collected_amount': float(payment_performance.collected_amount or 0)
            },
            'generated_at': datetime.utcnow().isoformat()
        }  
  
    @staticmethod
    def generate_customer_investigation_report(db: Session, customer_id: str) -> Dict[str, Any]:
        """Generate detailed customer investigation report"""
        
        # Get customer details
        customer = db.query(User).filter(User.id == customer_id).first()
        
        # Get complete installment history
        installment_history = db.query(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id
        ).order_by(InstallmentPlan.created_at.desc()).all()
        
        # Get all fraud alerts
        fraud_alerts = db.query(FraudAlert).filter(
            FraudAlert.customer_id == customer_id
        ).order_by(FraudAlert.created_at.desc()).all()
        
        # Get all fraud patterns
        fraud_patterns = db.query(FraudPattern).filter(
            FraudPattern.customer_id == customer_id
        ).order_by(FraudPattern.detected_at.desc()).all()
        
        # Analyze business relationships
        business_relationships = db.query(
            Business.id,
            Business.business_name,
            func.count(InstallmentPlan.id).label('plan_count'),
            func.sum(InstallmentPlan.total_amount).label('total_amount'),
            func.min(InstallmentPlan.created_at).label('first_plan'),
            func.max(InstallmentPlan.created_at).label('last_plan')
        ).join(InstallmentPlan).filter(
            InstallmentPlan.customer_id == customer_id
        ).group_by(Business.id, Business.business_name).all()
        
        # Calculate timeline of activities
        timeline = []
        
        # Add installment plans to timeline
        for plan in installment_history:
            timeline.append({
                'date': plan.created_at.isoformat(),
                'type': 'installment_plan',
                'description': f"Installment plan created for ${plan.total_amount}",
                'status': plan.status.value,
                'business_id': str(plan.business_id)
            })
        
        # Add fraud alerts to timeline
        for alert in fraud_alerts:
            timeline.append({
                'date': alert.created_at.isoformat(),
                'type': 'fraud_alert',
                'description': alert.description,
                'severity': alert.severity.value,
                'alert_type': alert.alert_type.value
            })
        
        # Sort timeline by date
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
        return {
            'report_type': 'customer_investigation',
            'customer': {
                'id': str(customer.id),
                'name': f"{customer.first_name} {customer.last_name}",
                'email': customer.email,
                'phone': customer.phone,
                'role': customer.role.value,
                'created_at': customer.created_at.isoformat(),
                'is_active': customer.is_active
            },
            'summary': {
                'total_installment_plans': len(installment_history),
                'total_fraud_alerts': len(fraud_alerts),
                'total_fraud_patterns': len(fraud_patterns),
                'business_relationships': len(business_relationships),
                'total_installment_value': sum(float(plan.total_amount) for plan in installment_history),
                'total_outstanding': sum(float(plan.remaining_amount) for plan in installment_history if plan.status == PlanStatus.ACTIVE)
            },
            'installment_history': [
                {
                    'id': str(plan.id),
                    'business_id': str(plan.business_id),
                    'total_amount': float(plan.total_amount),
                    'paid_amount': float(plan.paid_amount),
                    'remaining_amount': float(plan.remaining_amount),
                    'status': plan.status.value,
                    'created_at': plan.created_at.isoformat()
                }
                for plan in installment_history
            ],
            'fraud_alerts': [
                {
                    'id': str(alert.id),
                    'alert_type': alert.alert_type.value,
                    'severity': alert.severity.value,
                    'status': alert.status.value,
                    'description': alert.description,
                    'created_at': alert.created_at.isoformat(),
                    'metadata': alert.alert_metadata
                }
                for alert in fraud_alerts
            ],
            'business_relationships': [
                {
                    'business_id': str(rel.id),
                    'business_name': rel.business_name,
                    'plan_count': rel.plan_count,
                    'total_amount': float(rel.total_amount or 0),
                    'first_plan': rel.first_plan.isoformat(),
                    'last_plan': rel.last_plan.isoformat()
                }
                for rel in business_relationships
            ],
            'timeline': timeline[:50],  # Limit to 50 most recent events
            'generated_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def generate_business_investigation_report(db: Session, business_id: str) -> Dict[str, Any]:
        """Generate detailed business investigation report"""
        
        # Get business details
        business = db.query(Business).filter(Business.id == business_id).first()
        
        # Get business performance metrics
        performance_metrics = db.query(
            func.count(InstallmentRequest.id).label('total_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.APPROVED, True)).label('approved_requests'),
            func.count(func.nullif(InstallmentRequest.status != RequestStatus.REJECTED, True)).label('rejected_requests'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.COMPLETED, True)).label('completed_plans'),
            func.count(func.nullif(InstallmentPlan.status != PlanStatus.DEFAULTED, True)).label('defaulted_plans'),
            func.coalesce(func.sum(InstallmentPlan.total_amount), 0).label('total_revenue'),
            func.coalesce(func.sum(InstallmentPlan.paid_amount), 0).label('collected_amount'),
            func.count(func.distinct(InstallmentRequest.customer_id)).label('unique_customers')
        ).outerjoin(InstallmentRequest).outerjoin(InstallmentPlan).filter(
            InstallmentRequest.business_id == business_id
        ).first()
        
        # Get top customers by volume
        top_customers = db.query(
            User.id,
            User.first_name,
            User.last_name,
            User.email,
            func.count(InstallmentPlan.id).label('plan_count'),
            func.sum(InstallmentPlan.total_amount).label('total_amount')
        ).join(InstallmentPlan).filter(
            InstallmentPlan.business_id == business_id
        ).group_by(User.id, User.first_name, User.last_name, User.email).order_by(
            func.sum(InstallmentPlan.total_amount).desc()
        ).limit(20).all()
        
        # Get recent activity
        recent_requests = db.query(InstallmentRequest).filter(
            InstallmentRequest.business_id == business_id,
            InstallmentRequest.created_at >= datetime.utcnow() - timedelta(days=30)
        ).order_by(InstallmentRequest.created_at.desc()).limit(50).all()
        
        # Calculate derived metrics
        approval_rate = (performance_metrics.approved_requests / performance_metrics.total_requests * 100) if performance_metrics.total_requests > 0 else 0
        default_rate = (performance_metrics.defaulted_plans / performance_metrics.approved_requests * 100) if performance_metrics.approved_requests > 0 else 0
        collection_rate = (float(performance_metrics.collected_amount) / float(performance_metrics.total_revenue) * 100) if performance_metrics.total_revenue > 0 else 0
        
        return {
            'report_type': 'business_investigation',
            'business': {
                'id': str(business.id),
                'name': business.business_name,
                'type': business.business_type,
                'is_verified': business.is_verified,
                'created_at': business.created_at.isoformat(),
                'owner_id': str(business.owner_id)
            },
            'performance_summary': {
                'total_requests': performance_metrics.total_requests,
                'approved_requests': performance_metrics.approved_requests,
                'rejected_requests': performance_metrics.rejected_requests,
                'approval_rate': round(approval_rate, 2),
                'completed_plans': performance_metrics.completed_plans,
                'defaulted_plans': performance_metrics.defaulted_plans,
                'default_rate': round(default_rate, 2),
                'total_revenue': float(performance_metrics.total_revenue),
                'collected_amount': float(performance_metrics.collected_amount),
                'collection_rate': round(collection_rate, 2),
                'unique_customers': performance_metrics.unique_customers
            },
            'top_customers': [
                {
                    'customer_id': str(customer.id),
                    'customer_name': f"{customer.first_name} {customer.last_name}",
                    'customer_email': customer.email,
                    'plan_count': customer.plan_count,
                    'total_amount': float(customer.total_amount or 0)
                }
                for customer in top_customers
            ],
            'recent_activity': [
                {
                    'request_id': str(request.id),
                    'customer_id': str(request.customer_id),
                    'product_name': request.product_name,
                    'product_value': float(request.product_value),
                    'status': request.status.value,
                    'created_at': request.created_at.isoformat()
                }
                for request in recent_requests
            ],
            'generated_at': datetime.utcnow().isoformat()
        }    

    @staticmethod
    def export_fraud_data(db: Session, days: int, format: str) -> Dict[str, Any]:
        """Export fraud detection data for external analysis"""
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get fraud data
        fraud_data = db.query(
            FraudAlert.id,
            FraudAlert.customer_id,
            FraudAlert.alert_type,
            FraudAlert.severity,
            FraudAlert.status,
            FraudAlert.description,
            FraudAlert.created_at,
            User.email,
            User.first_name,
            User.last_name
        ).join(User).filter(
            FraudAlert.created_at >= cutoff_date
        ).order_by(FraudAlert.created_at.desc()).all()
        
        if format == "json":
            export_data = {
                'export_type': 'fraud_data',
                'period_days': days,
                'format': 'json',
                'data': [
                    {
                        'alert_id': str(alert.id),
                        'customer_id': str(alert.customer_id),
                        'customer_email': alert.email,
                        'customer_name': f"{alert.first_name} {alert.last_name}",
                        'alert_type': alert.alert_type.value,
                        'severity': alert.severity.value,
                        'status': alert.status.value,
                        'description': alert.description,
                        'created_at': alert.created_at.isoformat()
                    }
                    for alert in fraud_data
                ],
                'total_records': len(fraud_data),
                'exported_at': datetime.utcnow().isoformat()
            }
        else:  # CSV format
            output = StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Alert ID', 'Customer ID', 'Customer Email', 'Customer Name',
                'Alert Type', 'Severity', 'Status', 'Description', 'Created At'
            ])
            
            # Write data
            for alert in fraud_data:
                writer.writerow([
                    str(alert.id),
                    str(alert.customer_id),
                    alert.email,
                    f"{alert.first_name} {alert.last_name}",
                    alert.alert_type.value,
                    alert.severity.value,
                    alert.status.value,
                    alert.description,
                    alert.created_at.isoformat()
                ])
            
            export_data = {
                'export_type': 'fraud_data',
                'period_days': days,
                'format': 'csv',
                'csv_data': output.getvalue(),
                'total_records': len(fraud_data),
                'exported_at': datetime.utcnow().isoformat()
            }
            
            output.close()
        
        return export_data