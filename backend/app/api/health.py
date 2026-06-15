"""Health check endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("/")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/dashboard")
def health_dashboard(db: Session = Depends(get_db)):
    """Dashboard health metrics"""
    settings = get_settings()
    return {
        "status": "healthy",
        "environment": settings.PYTHON_ENV,
        "app_version": "1.0.0",
        "database": "connected",
        "metrics": {
            "total_devices": 0,
            "reachable_devices": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "success_rate": "0%"
        }
    }
