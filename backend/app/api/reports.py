"""Report endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.report import ReportGenerateRequest, ReportResponse, ReportListResponse
from app.services.report import ReportService

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(request: ReportGenerateRequest, db: Session = Depends(get_db)):
    """Generate test report"""
    try:
        report = ReportService.generate_report(db, request)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ReportListResponse)
def list_reports(db: Session = Depends(get_db)):
    """List all reports"""
    reports = ReportService.get_all_reports(db)
    return {"total": len(reports), "reports": reports}


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get report by ID"""
    report = ReportService.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/{report_id}/export")
def export_report(report_id: int, format: str = "html", db: Session = Depends(get_db)):
    """Export report in specified format"""
    report = ReportService.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        content = ReportService.export_report(report, format)
        return {"content": content, "format": format}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
