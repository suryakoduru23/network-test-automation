"""Alert Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import BaseModel


class AlertSeverity(PyEnum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(PyEnum):
    """Alert status"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Alert(BaseModel):
    """Alert Model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    title = Column(String(255), index=True)
    description = Column(Text)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.WARNING)
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    triggered_at = Column(DateTime)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    is_notified = Column(Boolean, default=False)
    
    # Relationships
    device = relationship("Device", back_populates="alerts")
    
    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, title={self.title}, severity={self.severity})>"
