"""Report Schemas"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ReportFormat(str, Enum):
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"


class ReportStatus(str, Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportGenerateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    report_format: ReportFormat = ReportFormat.HTML
    start_date: datetime
    end_date: datetime
    test_case_ids: Optional[list] = None
    device_ids: Optional[list] = None


class ReportResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    report_format: ReportFormat
    status: ReportStatus
    file_path: Optional[str] = None
    generated_at: Optional[datetime] = None
    start_date: datetime
    end_date: datetime
    test_count: int
    passed_count: int
    failed_count: int
    success_rate: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    total: int
    reports: List[ReportResponse]


class ReportExportRequest(BaseModel):
    report_format: ReportFormat
