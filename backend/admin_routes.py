"""
Superadmin dashboard and reporting routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, text
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, timedelta
from decimal import Decimal

from database import get_db
from auth import get_current_superadmin
from models import (
    User, Business, InstallmentRequest, InstallmentPlan, Payment,
    FraudAlert, FraudPattern, UserRole, RequestStatus, PlanStatus,
    PaymentStatus, AlertType, AlertSeverity, AlertStatus
)
from admin_service import AdminDashboardService, ReportingService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/dashboard/overview")
async def get_dashboard_overview(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get comprehensive system overview for superadmin dashboard"""
    
    try:
        overview = AdminDashboardService.get_system_overview(db)
        
        logger.info(f"Dashboard overview accessed by superadmin {current_user.email}")
        
        return overview
        
    except Exception as e:
        logger.error(f"Error generating dashboard overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate dashboard overview"
        )

@router.get("/dashboard/metrics")
async def get_system_metrics(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get detailed system metrics for specified period"""
    
    try:
        # Parse period
        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "1y": 365
        }[period]
        
        metrics = AdminDashboardService.get_system_metrics(db, period_days)
        
        logger.info(f"System metrics accessed for {period} by superadmin {current_user.email}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error generating system metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate system metrics"
        )

@router.get("/dashboard/fraud-summary")
async def get_fraud_summary(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get comprehensive fraud detection summary"""
    
    try:
        fraud_summary = AdminDashboardService.get_fraud_summary(db)
        
        logger.info(f"Fraud summary accessed by superadmin {current_user.email}")
        
        return fraud_summary
        
    except Exception as e:
        logger.error(f"Error generating fraud summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate fraud summary"
        )

@router.get("/dashboard/business-analytics")
async def get_business_analytics(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get business participation and performance analytics"""
    
    try:
        analytics = AdminDashboardService.get_business_analytics(db)
        
        logger.info(f"Business analytics accessed by superadmin {current_user.email}")
        
        return analytics
        
    except Exception as e:
        logger.error(f"Error generating business analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate business analytics"
        )

@router.get("/reports/fraud-trends")
async def get_fraud_trends_report(
    days: int = Query(30, ge=1, le=365),
    granularity: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate fraud trends report"""
    
    try:
        report = ReportingService.generate_fraud_trends_report(db, days, granularity)
        
        logger.info(f"Fraud trends report generated for {days} days by superadmin {current_user.email}")
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating fraud trends report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate fraud trends report"
        )

@router.get("/reports/business-performance")
async def get_business_performance_report(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    sort_by: str = Query("total_revenue", regex="^(total_revenue|approval_rate|default_rate|customer_count)$"),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate business performance report"""
    
    try:
        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "1y": 365
        }[period]
        
        report = ReportingService.generate_business_performance_report(
            db, period_days, sort_by, limit
        )
        
        logger.info(f"Business performance report generated by superadmin {current_user.email}")
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating business performance report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate business performance report"
        )

@router.get("/reports/customer-risk-analysis")
async def get_customer_risk_analysis_report(
    risk_threshold: float = Query(0.7, ge=0, le=1),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate customer risk analysis report"""
    
    try:
        report = ReportingService.generate_customer_risk_analysis_report(
            db, risk_threshold, limit
        )
        
        logger.info(f"Customer risk analysis report generated by superadmin {current_user.email}")
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating customer risk analysis report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate customer risk analysis report"
        )

@router.get("/reports/financial-overview")
async def get_financial_overview_report(
    period: str = Query("30d", regex="^(7d|30d|90d|1y)$"),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate financial overview report"""
    
    try:
        period_days = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "1y": 365
        }[period]
        
        report = ReportingService.generate_financial_overview_report(db, period_days)
        
        logger.info(f"Financial overview report generated by superadmin {current_user.email}")
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating financial overview report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate financial overview report"
        )

@router.get("/analytics/cross-business-patterns")
async def get_cross_business_patterns(
    min_businesses: int = Query(3, ge=2, le=10),
    days: int = Query(90, ge=1, le=365),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Analyze cross-business installment patterns"""
    
    try:
        patterns = AdminDashboardService.analyze_cross_business_patterns(
            db, min_businesses, days
        )
        
        logger.info(f"Cross-business patterns analyzed by superadmin {current_user.email}")
        
        return patterns
        
    except Exception as e:
        logger.error(f"Error analyzing cross-business patterns: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze cross-business patterns"
        )

@router.get("/analytics/fraud-effectiveness")
async def get_fraud_detection_effectiveness(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Analyze fraud detection system effectiveness"""
    
    try:
        effectiveness = AdminDashboardService.analyze_fraud_detection_effectiveness(db)
        
        logger.info(f"Fraud detection effectiveness analyzed by superadmin {current_user.email}")
        
        return effectiveness
        
    except Exception as e:
        logger.error(f"Error analyzing fraud detection effectiveness: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze fraud detection effectiveness"
        )

@router.get("/investigation/customer/{customer_id}")
async def get_customer_investigation_report(
    customer_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate detailed customer investigation report"""
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    try:
        investigation = ReportingService.generate_customer_investigation_report(
            db, customer_id
        )
        
        logger.info(f"Customer investigation report generated for {customer_id} by superadmin {current_user.email}")
        
        return investigation
        
    except Exception as e:
        logger.error(f"Error generating customer investigation report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate customer investigation report"
        )

@router.get("/investigation/business/{business_id}")
async def get_business_investigation_report(
    business_id: str,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Generate detailed business investigation report"""
    
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    try:
        investigation = ReportingService.generate_business_investigation_report(
            db, business_id
        )
        
        logger.info(f"Business investigation report generated for {business_id} by superadmin {current_user.email}")
        
        return investigation
        
    except Exception as e:
        logger.error(f"Error generating business investigation report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate business investigation report"
        )

@router.get("/system/health")
async def get_system_health(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get comprehensive system health status"""
    
    try:
        health = AdminDashboardService.get_system_health(db)
        
        logger.info(f"System health checked by superadmin {current_user.email}")
        
        return health
        
    except Exception as e:
        logger.error(f"Error checking system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check system health"
        )

@router.get("/system/configuration")
async def get_system_configuration(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get current system configuration and thresholds"""
    
    try:
        config = AdminDashboardService.get_system_configuration(db)
        
        logger.info(f"System configuration accessed by superadmin {current_user.email}")
        
        return config
        
    except Exception as e:
        logger.error(f"Error getting system configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get system configuration"
        )

@router.post("/system/configuration")
async def update_system_configuration(
    config_updates: Dict[str, Any],
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Update system configuration and thresholds"""
    
    try:
        updated_config = AdminDashboardService.update_system_configuration(
            db, config_updates, current_user.email
        )
        
        logger.info(f"System configuration updated by superadmin {current_user.email}")
        
        return {
            "message": "System configuration updated successfully",
            "updated_config": updated_config,
            "updated_by": current_user.email,
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating system configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update system configuration"
        )

@router.get("/exports/fraud-data")
async def export_fraud_data(
    format: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Export fraud detection data for external analysis"""
    
    try:
        export_data = ReportingService.export_fraud_data(db, days, format)
        
        logger.info(f"Fraud data exported in {format} format by superadmin {current_user.email}")
        
        return export_data
        
    except Exception as e:
        logger.error(f"Error exporting fraud data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export fraud data"
        )

@router.get("/alerts/critical")
async def get_critical_alerts(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get critical fraud alerts requiring immediate attention"""
    
    try:
        critical_alerts = AdminDashboardService.get_critical_alerts(db, limit)
        
        logger.info(f"Critical alerts accessed by superadmin {current_user.email}")
        
        return critical_alerts
        
    except Exception as e:
        logger.error(f"Error getting critical alerts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get critical alerts"
        )

@router.get("/monitoring/real-time")
async def get_real_time_monitoring(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get real-time system monitoring data"""
    
    try:
        monitoring_data = AdminDashboardService.get_real_time_monitoring(db)
        
        return monitoring_data
        
    except Exception as e:
        logger.error(f"Error getting real-time monitoring data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get real-time monitoring data"
        )