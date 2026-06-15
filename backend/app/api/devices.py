"""Device endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse, DeviceStatusResponse
from app.services.device import DeviceService
from app.core.exceptions import ResourceNotFoundError, ValidationError

router = APIRouter(prefix="/api/v1/devices", tags=["Devices"])


@router.post("/", response_model=DeviceResponse)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    """Create new device"""
    try:
        db_device = DeviceService.create_device(db, device)
        return db_device
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get("/", response_model=List[DeviceResponse])
def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all devices"""
    devices = DeviceService.get_all_devices(db, skip, limit)
    return devices


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    """Get device by ID"""
    try:
        device = DeviceService.get_device(db, device_id)
        return device
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device_update: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """Update device"""
    try:
        updated_device = DeviceService.update_device(db, device_id, device_update)
        return updated_device
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Delete device"""
    try:
        DeviceService.delete_device(db, device_id)
        return {"message": "Device deleted successfully"}
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post("/{device_id}/test-connectivity", response_model=dict)
def test_device_connectivity(device_id: int, db: Session = Depends(get_db)):
    """Test device SSH connectivity"""
    try:
        is_reachable = DeviceService.test_device_connectivity(db, device_id)
        return {"device_id": device_id, "is_reachable": is_reachable}
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/site/{site}", response_model=List[DeviceResponse])
def get_devices_by_site(site: str, db: Session = Depends(get_db)):
    """Get devices by site"""
    devices = DeviceService.get_devices_by_site(db, site)
    return devices


@router.get("/status/reachable", response_model=List[DeviceStatusResponse])
def get_reachable_devices(db: Session = Depends(get_db)):
    """Get all reachable devices"""
    devices = DeviceService.get_reachable_devices(db)
    return devices
