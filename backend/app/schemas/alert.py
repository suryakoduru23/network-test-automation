"""Alert Schemas"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlertUpdateRequest(BaseModel):
    status: Optional[AlertStatus] = None
    acknowledged_at: Optional[datetime] = None


class AlertListResponse(BaseModel):
    total: int
    alerts: List[AlertResponse]
    critical_count: int
    warning_count: int
    info_count: int
