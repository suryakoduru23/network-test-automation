"""SSH Connection Service"""
import asyncio
from typing import Optional, List, Dict, Any
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from app.config import get_settings
from app.core.exceptions import SSHConnectionError
import logging

logger = logging.getLogger(__name__)


class SSHService:
    """SSH Connection and Command Execution Service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.connections: Dict[str, ConnectHandler] = {}
    
    def connect(
        self,
        hostname: str,
        ip_address: str,
        username: str,
        password: str,
        device_type: str,
        port: int = 22,
        timeout: int = 30
    ) -> bool:
        """Establish SSH connection to device"""
        try:
            device_params = {
                "device_type": device_type,
                "host": ip_address,
                "username": username,
                "password": password,
                "port": port,
                "timeout": timeout,
                "global_delay_factor": 0.1,
            }
            
            connection = ConnectHandler(**device_params)
            self.connections[hostname] = connection
            logger.info(f"Connected to device: {hostname}")
            return True
            
        except NetmikoAuthenticationException as e:
            logger.error(f"Authentication failed for {hostname}: {str(e)}")
            raise SSHConnectionError(f"Authentication failed for {hostname}")
        except NetmikoTimeoutException as e:
            logger.error(f"Connection timeout for {hostname}: {str(e)}")
            raise SSHConnectionError(f"Connection timeout for {hostname}")
        except Exception as e:
            logger.error(f"Connection error for {hostname}: {str(e)}")
            raise SSHConnectionError(f"Connection failed for {hostname}: {str(e)}")
    
    def disconnect(self, hostname: str) -> None:
        """Close SSH connection"""
        if hostname in self.connections:
            try:
                self.connections[hostname].disconnect()
                del self.connections[hostname]
                logger.info(f"Disconnected from device: {hostname}")
            except Exception as e:
                logger.error(f"Error disconnecting from {hostname}: {str(e)}")
    
    def execute_command(
        self,
        hostname: str,
        command: str
    ) -> str:
        """Execute command on device"""
        if hostname not in self.connections:
            raise SSHConnectionError(f"Not connected to device: {hostname}")
        
        try:
            output = self.connections[hostname].send_command(command)
            logger.debug(f"Command executed on {hostname}: {command}")
            return output
        except Exception as e:
            logger.error(f"Command execution error on {hostname}: {str(e)}")
            raise SSHConnectionError(f"Command execution failed on {hostname}")
    
    def execute_commands(
        self,
        hostname: str,
        commands: List[str]
    ) -> List[str]:
        """Execute multiple commands on device"""
        results = []
        for command in commands:
            try:
                output = self.execute_command(hostname, command)
                results.append(output)
            except Exception as e:
                logger.error(f"Error executing commands on {hostname}: {str(e)}")
                results.append(f"ERROR: {str(e)}")
        return results
    
    def send_config(
        self,
        hostname: str,
        config: List[str]
    ) -> str:
        """Send configuration commands to device"""
        if hostname not in self.connections:
            raise SSHConnectionError(f"Not connected to device: {hostname}")
        
        try:
            output = self.connections[hostname].send_config_set(config)
            logger.info(f"Configuration sent to {hostname}")
            return output
        except Exception as e:
            logger.error(f"Configuration error on {hostname}: {str(e)}")
            raise SSHConnectionError(f"Configuration failed on {hostname}")
    
    def is_connected(self, hostname: str) -> bool:
        """Check if device is connected"""
        return hostname in self.connections


# Global SSH service instance
ssh_service = SSHService()
