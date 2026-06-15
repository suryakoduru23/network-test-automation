"""Test Execution Service"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from app.models import TestRun, TestResult, TestCase, Device
from app.schemas.test import TestRunRequest
from app.core.exceptions import TestExecutionError
from app.services.validators import (
    InterfaceValidator, RouteValidator, DNSValidator, DHCPValidator,
    ARPValidator, VLANValidator, BGPValidator, OSPFValidator,
    ReachabilityValidator
)
import logging

logger = logging.getLogger(__name__)


class TestService:
    """Test Execution Service"""
    
    @staticmethod
    def run_test(db: Session, test_run_id: int) -> TestRun:
        """Execute a test"""
        test_run = db.query(TestRun).filter(TestRun.id == test_run_id).first()
        if not test_run:
            raise TestExecutionError(f"Test run {test_run_id} not found")
        
        try:
            test_run.status = "running"
            test_run.started_at = datetime.utcnow()
            db.commit()
            
            device = test_run.device
            test_case = test_run.test_case
            
            # Execute validator based on test type
            result = TestService._execute_validator(
                device.hostname,
                test_case.test_type
            )
            
            # Store result
            test_result = TestResult(
                test_run_id=test_run_id,
                passed=result["passed"],
                message=result["message"],
                output=result.get("output", {})
            )
            db.add(test_result)
            
            # Update test run
            test_run.status = "passed" if result["passed"] else "failed"
            test_run.completed_at = datetime.utcnow()
            duration = (test_run.completed_at - test_run.started_at).total_seconds()
            test_run.duration_seconds = int(duration)
            
            db.commit()
            db.refresh(test_run)
            logger.info(f"Test run {test_run_id} completed")
            return test_run
            
        except Exception as e:
            test_run.status = "error"
            test_run.completed_at = datetime.utcnow()
            db.commit()
            logger.error(f"Test run {test_run_id} failed: {str(e)}")
            raise TestExecutionError(f"Test execution failed: {str(e)}")
    
    @staticmethod
    def _execute_validator(hostname: str, test_type: str) -> Dict[str, Any]:
        """Execute appropriate validator"""
        validators_map = {
            "interface_validation": InterfaceValidator,
            "route_validation": RouteValidator,
            "dns_validation": DNSValidator,
            "dhcp_validation": DHCPValidator,
            "arp_validation": ARPValidator,
            "vlan_validation": VLANValidator,
            "bgp_validation": BGPValidator,
            "ospf_validation": OSPFValidator,
            "reachability_test": ReachabilityValidator,
        }
        
        validator_class = validators_map.get(test_type)
        if not validator_class:
            raise TestExecutionError(f"Unknown test type: {test_type}")
        
        # Initialize validator (default parameters for demo)
        validator = validator_class(hostname, "eth0")
        return validator.validate()
    
    @staticmethod
    def run_bulk_tests(db: Session, test_run_ids: List[int]) -> List[TestRun]:
        """Run multiple tests"""
        results = []
        for test_run_id in test_run_ids:
            try:
                result = TestService.run_test(db, test_run_id)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to run test {test_run_id}: {str(e)}")
        return results
