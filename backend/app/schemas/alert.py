"""Alert Schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class AlertResponse(BaseModel):
    id: int
    device_id: int
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    triggered_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    is_notified: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AlertUpdateRequest(BaseModel):
    status: Optional[AlertStatus] = None
    acknowledged_at: Optional[datetime] = None


class AlertListResponse(BaseModel):
    total: int
    alerts: list
    critical_count: int
    warning_count: int
    info_count: int
