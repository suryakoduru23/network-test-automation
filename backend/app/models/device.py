"""Device Model"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.models.base import BaseModel


class DeviceType(PyEnum):
    """Device types"""
    ROUTER = "router"
    SWITCH = "switch"
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"


class DeviceOS(PyEnum):
    """Device operating systems"""
    CISCO_IOS = "cisco_ios"
    CISCO_IOSXE = "cisco_iosxe"
    CISCO_IOSXR = "cisco_iosxr"
    JUNIPER_JUNOS = "juniper_junos"
    ARISTA_EOS = "arista_eos"
    LINUX = "linux"


class Device(BaseModel):
    """Device Model"""
    __tablename__ = "devices"
    __table_args__ = (
        Index('idx_device_hostname_site', 'hostname', 'site'),
        Index('idx_device_type', 'device_type'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(255), unique=True, index=True)
    ip_address = Column(String(255), index=True)
    device_type = Column(Enum(DeviceType), default=DeviceType.ROUTER)
    os_type = Column(Enum(DeviceOS), default=DeviceOS.CISCO_IOS)
    username = Column(String(255))
    password = Column(String(255))
    ssh_key_path = Column(String(255), nullable=True)
    ssh_port = Column(Integer, default=22)
    site = Column(String(255), index=True)
    location = Column(String(255))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    is_reachable = Column(Boolean, default=False)
    last_check_time = Column(String(255), nullable=True)
    
    # Relationships
    test_runs = relationship("TestRun", back_populates="device")
    alerts = relationship("Alert", back_populates="device")
    
    def __repr__(self) -> str:
        return f"<Device(id={self.id}, hostname={self.hostname}, ip={self.ip_address})>"
