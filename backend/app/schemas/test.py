"""Test Schemas"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TestType(str, Enum):
    INTERFACE_VALIDATION = "interface_validation"
    ROUTE_VALIDATION = "route_validation"
    DNS_VALIDATION = "dns_validation"
    DHCP_VALIDATION = "dhcp_validation"
    ARP_VALIDATION = "arp_validation"
    VLAN_VALIDATION = "vlan_validation"
    BGP_VALIDATION = "bgp_validation"
    OSPF_VALIDATION = "ospf_validation"
    REACHABILITY_TEST = "reachability_test"


class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"


class TestCaseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    test_type: TestType
    expected_result: str
    timeout_seconds: int = Field(30, ge=1)
    retry_count: int = Field(0, ge=0)


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseResponse(TestCaseBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TestRunRequest(BaseModel):
    test_case_id: int
    device_id: int


class TestRunResponse(BaseModel):
    id: int
    test_case_id: int
    device_id: int
    status: TestStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TestResultResponse(BaseModel):
    id: int
    test_run_id: int
    passed: bool
    message: str
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    output: Optional[dict] = None

    class Config:
        from_attributes = True


class TestRunDetailResponse(TestRunResponse):
    results: List[TestResultResponse] = Field(default_factory=list)


class BulkTestRunRequest(BaseModel):
    test_case_ids: List[int]
    device_ids: List[int]
