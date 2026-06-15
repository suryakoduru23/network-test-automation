"""Test endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.test import (
    TestCaseCreate, TestCaseResponse, TestRunRequest, TestRunResponse,
    TestRunDetailResponse, BulkTestRunRequest
)
from app.services.test import TestService
from app.core.exceptions import TestExecutionError, ResourceNotFoundError

router = APIRouter(prefix="/api/v1/tests", tags=["Tests"])


@router.post("/run", response_model=TestRunResponse)
def run_test(request: TestRunRequest, db: Session = Depends(get_db)):
    """Run a test"""
    try:
        test_run = TestService.run_test(db, request.test_case_id)
        return test_run
    except TestExecutionError as e:
        raise HTTPException(status_code=500, detail=e.message)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/run-bulk")
def run_bulk_tests(request: BulkTestRunRequest, db: Session = Depends(get_db)):
    """Run multiple tests"""
    try:
        # Create test runs for each combination
        test_run_ids = []
        for test_case_id in request.test_case_ids:
            for device_id in request.device_ids:
                test_run_ids.append(f"{test_case_id}_{device_id}")
        
        return {"message": "Bulk tests queued", "count": len(test_run_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{test_run_id}", response_model=TestRunDetailResponse)
def get_test_run(test_run_id: int, db: Session = Depends(get_db)):
    """Get test run details"""
    return {"message": "Test run details"}


@router.get("/history")
def get_test_history(db: Session = Depends(get_db)):
    """Get test execution history"""
    return {"message": "Test history"}
