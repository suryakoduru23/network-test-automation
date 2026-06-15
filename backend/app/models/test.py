"""Test Models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime
from app.models.base import BaseModel


class TestType(PyEnum):
    """Test types"""
    INTERFACE_VALIDATION = "interface_validation"
    ROUTE_VALIDATION = "route_validation"
    DNS_VALIDATION = "dns_validation"
    DHCP_VALIDATION = "dhcp_validation"
    ARP_VALIDATION = "arp_validation"
    VLAN_VALIDATION = "vlan_validation"
    BGP_VALIDATION = "bgp_validation"
    OSPF_VALIDATION = "ospf_validation"
    REACHABILITY_TEST = "reachability_test"


class TestStatus(PyEnum):
    """Test execution status"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


class TestCase(BaseModel):
    """Test Case Model"""
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    test_type = Column(Enum(TestType), index=True)
    expected_result = Column(Text)
    is_active = Column(Boolean, default=True)
    timeout_seconds = Column(Integer, default=30)
    retry_count = Column(Integer, default=0)
    
    # Relationships
    test_runs = relationship("TestRun", back_populates="test_case")
    
    def __repr__(self) -> str:
        return f"<TestCase(id={self.id}, name={self.name}, type={self.test_type})>"


class TestRun(BaseModel):
    """Test Run Model"""
    __tablename__ = "test_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    status = Column(Enum(TestStatus), default=TestStatus.PENDING, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    # Relationships
    test_case = relationship("TestCase", back_populates="test_runs")
    device = relationship("Device", back_populates="test_runs")
    results = relationship("TestResult", back_populates="test_run")
    
    def __repr__(self) -> str:
        return f"<TestRun(id={self.id}, status={self.status})>"


class TestResult(BaseModel):
    """Test Result Model"""
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    passed = Column(Boolean)
    message = Column(Text)
    expected_value = Column(Text)
    actual_value = Column(Text)
    output = Column(JSON)
    
    # Relationships
    test_run = relationship("TestRun", back_populates="results")
    
    def __repr__(self) -> str:
        return f"<TestResult(id={self.id}, passed={self.passed})>"
