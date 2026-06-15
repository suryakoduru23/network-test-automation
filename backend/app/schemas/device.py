"""Device schemas.

Credential fields are intentionally limited to create/update request models.
They must never be inherited by response schemas.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, SecretStr


class DeviceType(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"


class DeviceOS(str, Enum):
    CISCO_IOS = "cisco_ios"
    CISCO_IOSXE = "cisco_iosxe"
    CISCO_IOSXR = "cisco_iosxr"
    JUNIPER_JUNOS = "juniper_junos"
    ARISTA_EOS = "arista_eos"
    LINUX = "linux"


class DeviceBase(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=255)
    ip_address: str = Field(..., min_length=1, max_length=255)
    device_type: DeviceType
    os_type: DeviceOS
    ssh_port: int = Field(22, ge=1, le=65535)
    site: str
    location: Optional[str] = None
    description: Optional[str] = None


class DeviceCreate(DeviceBase):
    username: str = Field(..., min_length=1, max_length=255)
    password: SecretStr = Field(..., min_length=1, max_length=255)


class DeviceUpdate(BaseModel):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    device_type: Optional[DeviceType] = None
    os_type: Optional[DeviceOS] = None
    username: Optional[str] = None
    password: Optional[SecretStr] = None
    ssh_port: Optional[int] = Field(None, ge=1, le=65535)
    site: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    """Safe device response without passwords or secret material."""

    id: int
    username: str
    is_active: bool
    is_reachable: bool
    last_check_time: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DeviceStatusResponse(BaseModel):
    id: int
    hostname: str
    is_reachable: bool
    last_check_time: Optional[str] = None

    class Config:
        from_attributes = True
