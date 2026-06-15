"""Report Model"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import BaseModel


class ReportFormat(PyEnum):
    """Report formats"""
    HTML = "html"
    PDF = "pdf"
    CSV = "csv"


class ReportStatus(PyEnum):
    """Report generation status"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(BaseModel):
    """Report Model"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text)
    report_format = Column(Enum(ReportFormat), default=ReportFormat.HTML)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    file_path = Column(String(255), nullable=True)
    generated_at = Column(DateTime, nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    test_count = Column(Integer, default=0)
    passed_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    success_rate = Column(String(10), default="0%")
    
    def __repr__(self) -> str:
        return f"<Report(id={self.id}, title={self.title})>"
