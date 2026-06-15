"""Health check endpoints."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.database import get_db
from app.models import Device, TestRun, TestStatus

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


def _utc_now_iso() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _database_status(db: Session) -> dict:
    """Run a lightweight database connectivity probe."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected", "error": None}
    except SQLAlchemyError as exc:
        return {"status": "unavailable", "error": exc.__class__.__name__}


def _dashboard_metrics(db: Session) -> dict:
    """Build dashboard metrics from persisted inventory and test runs."""
    total_devices = db.query(Device).count()
    reachable_devices = db.query(Device).filter(Device.is_reachable.is_(True)).count()
    total_tests = db.query(TestRun).count()
    passed_tests = db.query(TestRun).filter(TestRun.status == TestStatus.PASSED).count()
    failed_tests = db.query(TestRun).filter(TestRun.status == TestStatus.FAILED).count()
    success_rate = (passed_tests / total_tests * 100) if total_tests else 0

    return {
        "total_devices": total_devices,
        "reachable_devices": reachable_devices,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": f"{success_rate:.1f}%",
    }


@router.get("/")
def health_check(db: Session = Depends(get_db)):
    """Return application and database health."""
    database = _database_status(db)
    is_healthy = database["status"] == "connected"

    return {
        "status": "healthy" if is_healthy else "degraded",
        "timestamp": _utc_now_iso(),
        "database": database,
    }


@router.get("/dashboard", status_code=status.HTTP_200_OK)
def health_dashboard(db: Session = Depends(get_db)):
    """Dashboard health metrics."""
    settings = get_settings()
    database = _database_status(db)
    metrics = _dashboard_metrics(db) if database["status"] == "connected" else {
        "total_devices": 0,
        "reachable_devices": 0,
        "total_tests": 0,
        "passed_tests": 0,
        "failed_tests": 0,
        "success_rate": "0.0%",
    }

    return {
        "status": "healthy" if database["status"] == "connected" else "degraded",
        "timestamp": _utc_now_iso(),
        "environment": settings.PYTHON_ENV,
        "app_version": settings.APP_VERSION,
        "database": database,
        "metrics": metrics,
    }
