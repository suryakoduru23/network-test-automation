import logging
from typing import List

from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models import Device
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.services.ssh import ssh_service

logger = logging.getLogger(__name__)


class DeviceService:
    """Device Management Service"""

    @staticmethod
    def _secret_to_string(value: SecretStr | str | None) -> str | None:
        """Convert write-only secret fields before persistence."""
        if isinstance(value, SecretStr):
            return value.get_secret_value()
        return value
    
    @staticmethod
    def create_device(db: Session, device: DeviceCreate) -> Device:
        """Create new device"""
        # Check if device already exists
        existing = db.query(Device).filter(
            Device.hostname == device.hostname
        ).first()
        if existing:
            raise ValidationError(f"Device with hostname {device.hostname} already exists")
        
        db_device = Device(
            hostname=device.hostname,
            ip_address=device.ip_address,
            device_type=device.device_type,
            os_type=device.os_type,
            username=device.username,
            password=DeviceService._secret_to_string(device.password),
            ssh_port=device.ssh_port,
            site=device.site,
            location=device.location,
            description=device.description,
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        logger.info(f"Device created: {device.hostname}")
        return db_device
    
    @staticmethod
    def get_device(db: Session, device_id: int) -> Device:
        """Get device by ID"""
        device = db.query(Device).filter(Device.id == device_id).first()
        if not device:
            raise ResourceNotFoundError(f"Device with ID {device_id} not found")
        return device
    
    @staticmethod
    def get_all_devices(db: Session, skip: int = 0, limit: int = 100) -> List[Device]:
        """Get all devices"""
        return db.query(Device).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_device(
        db: Session,
        device_id: int,
        device_update: DeviceUpdate
    ) -> Device:
        """Update device"""
        device = DeviceService.get_device(db, device_id)
        
        update_data = device_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password":
                value = DeviceService._secret_to_string(value)
            setattr(device, key, value)
        
        db.add(device)
        db.commit()
        db.refresh(device)
        logger.info(f"Device updated: {device.hostname}")
        return device
    
    @staticmethod
    def delete_device(db: Session, device_id: int) -> bool:
        """Delete device"""
        device = DeviceService.get_device(db, device_id)
        
        # Disconnect SSH if connected
        if ssh_service.is_connected(device.hostname):
            ssh_service.disconnect(device.hostname)
        
        db.delete(device)
        db.commit()
        logger.info(f"Device deleted: {device.hostname}")
        return True
    
    @staticmethod
    def test_device_connectivity(db: Session, device_id: int) -> bool:
        """Test device SSH connectivity"""
        device = DeviceService.get_device(db, device_id)
        
        try:
            ssh_service.connect(
                hostname=device.hostname,
                ip_address=device.ip_address,
                username=device.username,
                password=device.password,
                device_type=device.os_type.value,
                port=device.ssh_port,
                timeout=30
            )
            
            device.is_reachable = True
            device.last_check_time = "2024-01-01"  # Update with current time
            
            db.add(device)
            db.commit()
            
            ssh_service.disconnect(device.hostname)
            logger.info(f"Device connectivity test passed: {device.hostname}")
            return True
            
        except Exception as e:
            device.is_reachable = False
            db.add(device)
            db.commit()
            logger.error(f"Device connectivity test failed: {device.hostname}")
            return False
    
    @staticmethod
    def get_devices_by_site(db: Session, site: str) -> List[Device]:
        """Get all devices in a site"""
        return db.query(Device).filter(Device.site == site).all()
    
    @staticmethod
    def get_reachable_devices(db: Session) -> List[Device]:
        """Get all reachable devices"""
        return db.query(Device).filter(Device.is_reachable == True).all()
