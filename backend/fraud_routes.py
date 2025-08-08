"""
Fraud detection routes for the Installment Fraud Detection System
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, timedelta

from database import get_db
from auth import get_current_user, get_current_superadmin, get_current_business
from models import User, Business, FraudAlert, FraudPattern, UserRole, AlertStatus
from schemas import FraudAlertResponse, FraudPatternResponse, PaginatedResponse
from fraud_engine import FraudDetectionEngine, FraudRiskLevel
from fraud_service import FraudDetectionService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

@router.post("/analyze/{customer_id}")
async def analyze_customer_fraud_risk(
    customer_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform comprehensive fraud analysis on a customer"""
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER:
        if str(current_user.id) != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Customers can only analyze their own risk"
            )
    elif current_user.role == UserRole.BUSINESS:
        # Business users can analyze customers they have relationships with
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No business found for current user"
            )
        
        # Check if customer has interaction with this business
        from history_service import HistoryService
        has_interaction = HistoryService.customer_has_business_interaction(
            db, customer_id, str(user_business.id)
        )
        if not has_interaction:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No business relationship with this customer"
            )
    # Superadmins can analyze any customer
    
    # Verify customer exists
    customer = db.query(User).filter(User.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    try:
        # Initialize fraud detection engine
        fraud_engine = FraudDetectionEngine(db)
        
        # Perform analysis
        analysis_result = fraud_engine.analyze_customer(customer_id)
        
        # Schedule background tasks for additional processing
        background_tasks.add_task(
            _update_customer_risk_profile,
            db,
            customer_id,
            analysis_result
        )
        
        logger.info(f"Fraud analysis performed on customer {customer_id} by {current_user.role} {current_user.email}")
        
        return {
            "customer_id": analysis_result.customer_id,
            "risk_level": analysis_result.risk_level.value,
            "risk_score": analysis_result.risk_score,
            "detected_patterns": analysis_result.detected_patterns,
            "recommendations": analysis_result.recommendations,
            "should_block": analysis_result.should_block,
            "requires_manual_review": analysis_result.requires_manual_review,
            "confidence_score": analysis_result.confidence_score,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing customer {customer_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to perform fraud analysis"
        )

@router.get("/alerts", response_model=PaginatedResponse)
async def get_fraud_alerts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    severity: Optional[str] = None,
    status_filter: Optional[AlertStatus] = None,
    customer_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get fraud alerts with filtering"""
    
    query = db.query(FraudAlert)
    
    # Apply role-based filtering
    if current_user.role == UserRole.CUSTOMER:
        # Customers can only see their own alerts
        query = query.filter(FraudAlert.customer_id == current_user.id)
    elif current_user.role == UserRole.BUSINESS:
        # Business users can see alerts for customers they have relationships with
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if user_business:
            # Get customer IDs that have relationships with this business
            from history_service import HistoryService
            # This would need to be implemented to get all related customers
            # For now, we'll restrict to no alerts for business users
            query = query.filter(FraudAlert.id == None)  # No results
    # Superadmins can see all alerts
    
    # Apply filters
    if severity:
        query = query.filter(FraudAlert.severity == severity)
    
    if status_filter:
        query = query.filter(FraudAlert.status == status_filter)
    
    if customer_id and current_user.role == UserRole.SUPERADMIN:
        query = query.filter(FraudAlert.customer_id == customer_id)
    
    # Order by creation date (newest first)
    query = query.order_by(FraudAlert.created_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    alerts = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[FraudAlertResponse.from_orm(alert) for alert in alerts],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/alerts/{alert_id}", response_model=FraudAlertResponse)
async def get_fraud_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific fraud alert details"""
    
    alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fraud alert not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.CUSTOMER:
        if alert.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this alert"
            )
    elif current_user.role == UserRole.BUSINESS:
        # Business users can view alerts for customers they have relationships with
        user_business = db.query(Business).filter(Business.owner_id == current_user.id).first()
        if not user_business:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this alert"
            )
        
        from history_service import HistoryService
        has_interaction = HistoryService.customer_has_business_interaction(
            db, str(alert.customer_id), str(user_business.id)
        )
        if not has_interaction:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this alert"
            )
    # Superadmins can view any alert
    
    return FraudAlertResponse.from_orm(alert)

@router.put("/alerts/{alert_id}/status")
async def update_alert_status(
    alert_id: str,
    new_status: AlertStatus,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Update fraud alert status (superadmin only)"""
    
    alert = db.query(FraudAlert).filter(FraudAlert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fraud alert not found"
        )
    
    # Update alert status
    alert.status = new_status
    
    if new_status in [AlertStatus.RESOLVED, AlertStatus.FALSE_POSITIVE]:
        alert.resolved_at = datetime.utcnow()
    
    # Update metadata with notes if provided
    if notes:
        if not alert.alert_metadata:
            alert.alert_metadata = {}
        alert.alert_metadata["resolution_notes"] = notes
        alert.alert_metadata["resolved_by"] = current_user.email
    
    db.commit()
    
    logger.info(f"Fraud alert {alert_id} status updated to {new_status.value} by {current_user.email}")
    
    return {"message": "Alert status updated successfully"}

@router.get("/patterns", response_model=PaginatedResponse)
async def get_fraud_patterns(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    pattern_type: Optional[str] = None,
    customer_id: Optional[str] = None,
    min_risk_score: Optional[float] = Query(None, ge=0, le=1),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get fraud patterns (superadmin only)"""
    
    query = db.query(FraudPattern)
    
    # Apply filters
    if pattern_type:
        query = query.filter(FraudPattern.pattern_type == pattern_type)
    
    if customer_id:
        query = query.filter(FraudPattern.customer_id == customer_id)
    
    if min_risk_score is not None:
        query = query.filter(FraudPattern.risk_score >= min_risk_score)
    
    # Order by detection date (newest first)
    query = query.order_by(FraudPattern.detected_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    patterns = query.offset(offset).limit(size).all()
    
    # Calculate total pages
    pages = (total + size - 1) // size
    
    return PaginatedResponse(
        items=[FraudPatternResponse.from_orm(pattern) for pattern in patterns],
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.get("/dashboard")
async def get_fraud_dashboard(
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get fraud detection dashboard statistics"""
    
    try:
        # Get alert statistics
        alert_stats = db.query(
            FraudAlert.severity,
            FraudAlert.status,
            db.func.count(FraudAlert.id).label('count')
        ).group_by(FraudAlert.severity, FraudAlert.status).all()
        
        # Get recent high-risk customers
        recent_high_risk = db.query(FraudPattern).filter(
            FraudPattern.risk_score >= 0.7,
            FraudPattern.detected_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(FraudPattern.detected_at.desc()).limit(10).all()
        
        # Get pattern statistics
        pattern_stats = db.query(
            FraudPattern.pattern_type,
            db.func.count(FraudPattern.id).label('count'),
            db.func.avg(FraudPattern.risk_score).label('avg_risk_score')
        ).group_by(FraudPattern.pattern_type).all()
        
        # Format statistics
        alert_summary = {}
        for stat in alert_stats:
            severity = stat.severity.value
            status = stat.status.value
            if severity not in alert_summary:
                alert_summary[severity] = {}
            alert_summary[severity][status] = stat.count
        
        pattern_summary = {
            stat.pattern_type: {
                "count": stat.count,
                "avg_risk_score": float(stat.avg_risk_score)
            }
            for stat in pattern_stats
        }
        
        return {
            "alert_summary": alert_summary,
            "pattern_summary": pattern_summary,
            "recent_high_risk_customers": [
                {
                    "customer_id": str(pattern.customer_id),
                    "risk_score": float(pattern.risk_score),
                    "pattern_type": pattern.pattern_type,
                    "detected_at": pattern.detected_at.isoformat()
                }
                for pattern in recent_high_risk
            ],
            "dashboard_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating fraud dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate fraud dashboard"
        )

@router.post("/batch-analyze")
async def batch_analyze_customers(
    customer_ids: List[str],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Perform batch fraud analysis on multiple customers"""
    
    if len(customer_ids) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 customers can be analyzed in a batch"
        )
    
    # Verify all customers exist
    existing_customers = db.query(User.id).filter(User.id.in_(customer_ids)).all()
    existing_ids = {str(customer.id) for customer in existing_customers}
    
    missing_customers = set(customer_ids) - existing_ids
    if missing_customers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customers not found: {list(missing_customers)}"
        )
    
    # Schedule batch analysis as background task
    background_tasks.add_task(
        _perform_batch_analysis,
        db,
        customer_ids,
        current_user.email
    )
    
    logger.info(f"Batch fraud analysis scheduled for {len(customer_ids)} customers by {current_user.email}")
    
    return {
        "message": f"Batch analysis scheduled for {len(customer_ids)} customers",
        "customer_count": len(customer_ids),
        "scheduled_at": datetime.utcnow().isoformat()
    }

@router.get("/risk-trends")
async def get_risk_trends(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """Get fraud risk trends over time"""
    
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily risk pattern counts
        daily_patterns = db.query(
            db.func.date(FraudPattern.detected_at).label('date'),
            db.func.count(FraudPattern.id).label('pattern_count'),
            db.func.avg(FraudPattern.risk_score).label('avg_risk_score')
        ).filter(
            FraudPattern.detected_at >= cutoff_date
        ).group_by(
            db.func.date(FraudPattern.detected_at)
        ).order_by(
            db.func.date(FraudPattern.detected_at)
        ).all()
        
        # Get daily alert counts
        daily_alerts = db.query(
            db.func.date(FraudAlert.created_at).label('date'),
            FraudAlert.severity,
            db.func.count(FraudAlert.id).label('alert_count')
        ).filter(
            FraudAlert.created_at >= cutoff_date
        ).group_by(
            db.func.date(FraudAlert.created_at),
            FraudAlert.severity
        ).all()
        
        # Format trends data
        trends = {}
        for pattern in daily_patterns:
            date_str = pattern.date.isoformat()
            trends[date_str] = {
                "pattern_count": pattern.pattern_count,
                "avg_risk_score": float(pattern.avg_risk_score),
                "alerts": {}
            }
        
        for alert in daily_alerts:
            date_str = alert.date.isoformat()
            if date_str not in trends:
                trends[date_str] = {"pattern_count": 0, "avg_risk_score": 0, "alerts": {}}
            trends[date_str]["alerts"][alert.severity.value] = alert.alert_count
        
        return {
            "period_days": days,
            "trends": trends,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating risk trends: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate risk trends"
        )

# Background task functions
async def _update_customer_risk_profile(
    db: Session,
    customer_id: str,
    analysis_result
):
    """Background task to update customer risk profile"""
    
    try:
        # Update fraud patterns in the database
        FraudDetectionService.update_fraud_patterns(db, customer_id)
        
        logger.info(f"Customer risk profile updated for {customer_id}")
        
    except Exception as e:
        logger.error(f"Error updating risk profile for {customer_id}: {e}")

async def _perform_batch_analysis(
    db: Session,
    customer_ids: List[str],
    initiated_by: str
):
    """Background task to perform batch fraud analysis"""
    
    try:
        fraud_engine = FraudDetectionEngine(db)
        results = []
        
        for customer_id in customer_ids:
            try:
                result = fraud_engine.analyze_customer(customer_id)
                results.append({
                    "customer_id": customer_id,
                    "risk_level": result.risk_level.value,
                    "risk_score": result.risk_score
                })
            except Exception as e:
                logger.error(f"Error analyzing customer {customer_id} in batch: {e}")
                results.append({
                    "customer_id": customer_id,
                    "error": str(e)
                })
        
        logger.info(f"Batch analysis completed for {len(customer_ids)} customers by {initiated_by}")
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")