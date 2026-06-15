"""Test Validators"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.services.ssh import ssh_service
import logging

logger = logging.getLogger(__name__)


class BaseValidator(ABC):
    """Base validator class"""
    
    def __init__(self, hostname: str):
        self.hostname = hostname
    
    @abstractmethod
    def validate(self) -> Dict[str, Any]:
        """Validate test"""
        pass


class InterfaceValidator(BaseValidator):
    """Interface Validation"""
    
    def __init__(self, hostname: str, interface_name: str):
        super().__init__(hostname)
        self.interface_name = interface_name
    
    def validate(self) -> Dict[str, Any]:
        """Validate interface status"""
        try:
            command = f"show interface {self.interface_name}"
            output = ssh_service.execute_command(self.hostname, command)
            
            is_up = "up" in output.lower()
            return {
                "passed": is_up,
                "message": f"Interface {self.interface_name} is {'up' if is_up else 'down'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class RouteValidator(BaseValidator):
    """Route Validation"""
    
    def __init__(self, hostname: str, destination: str):
        super().__init__(hostname)
        self.destination = destination
    
    def validate(self) -> Dict[str, Any]:
        """Validate route exists"""
        try:
            command = f"show ip route {self.destination}"
            output = ssh_service.execute_command(self.hostname, command)
            
            route_exists = self.destination in output
            return {
                "passed": route_exists,
                "message": f"Route to {self.destination} {'found' if route_exists else 'not found'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class DNSValidator(BaseValidator):
    """DNS Validation"""
    
    def __init__(self, hostname: str, dns_server: str):
        super().__init__(hostname)
        self.dns_server = dns_server
    
    def validate(self) -> Dict[str, Any]:
        """Validate DNS server"""
        try:
            command = f"show ip name-server | include {self.dns_server}"
            output = ssh_service.execute_command(self.hostname, command)
            
            dns_configured = self.dns_server in output
            return {
                "passed": dns_configured,
                "message": f"DNS server {self.dns_server} {'configured' if dns_configured else 'not configured'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class DHCPValidator(BaseValidator):
    """DHCP Validation"""
    
    def __init__(self, hostname: str, interface_name: str):
        super().__init__(hostname)
        self.interface_name = interface_name
    
    def validate(self) -> Dict[str, Any]:
        """Validate DHCP lease"""
        try:
            command = f"show dhcp lease | include {self.interface_name}"
            output = ssh_service.execute_command(self.hostname, command)
            
            dhcp_active = "active" in output.lower() or self.interface_name in output
            return {
                "passed": dhcp_active,
                "message": f"DHCP on {self.interface_name} is {'active' if dhcp_active else 'inactive'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class ARPValidator(BaseValidator):
    """ARP Validation"""
    
    def __init__(self, hostname: str, ip_address: str):
        super().__init__(hostname)
        self.ip_address = ip_address
    
    def validate(self) -> Dict[str, Any]:
        """Validate ARP entry"""
        try:
            command = f"show arp | include {self.ip_address}"
            output = ssh_service.execute_command(self.hostname, command)
            
            arp_exists = self.ip_address in output
            return {
                "passed": arp_exists,
                "message": f"ARP entry for {self.ip_address} {'found' if arp_exists else 'not found'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class VLANValidator(BaseValidator):
    """VLAN Validation"""
    
    def __init__(self, hostname: str, vlan_id: int):
        super().__init__(hostname)
        self.vlan_id = vlan_id
    
    def validate(self) -> Dict[str, Any]:
        """Validate VLAN exists"""
        try:
            command = f"show vlan id {self.vlan_id}"
            output = ssh_service.execute_command(self.hostname, command)
            
            vlan_exists = str(self.vlan_id) in output
            return {
                "passed": vlan_exists,
                "message": f"VLAN {self.vlan_id} {'exists' if vlan_exists else 'does not exist'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class BGPValidator(BaseValidator):
    """BGP Neighbor Validation"""
    
    def __init__(self, hostname: str, neighbor_ip: str):
        super().__init__(hostname)
        self.neighbor_ip = neighbor_ip
    
    def validate(self) -> Dict[str, Any]:
        """Validate BGP neighbor"""
        try:
            command = "show ip bgp summary"
            output = ssh_service.execute_command(self.hostname, command)
            
            neighbor_up = self.neighbor_ip in output and "Established" in output
            return {
                "passed": neighbor_up,
                "message": f"BGP neighbor {self.neighbor_ip} is {'established' if neighbor_up else 'down'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class OSPFValidator(BaseValidator):
    """OSPF Neighbor Validation"""
    
    def __init__(self, hostname: str, neighbor_ip: str):
        super().__init__(hostname)
        self.neighbor_ip = neighbor_ip
    
    def validate(self) -> Dict[str, Any]:
        """Validate OSPF neighbor"""
        try:
            command = "show ip ospf neighbor"
            output = ssh_service.execute_command(self.hostname, command)
            
            neighbor_up = self.neighbor_ip in output and "FULL" in output
            return {
                "passed": neighbor_up,
                "message": f"OSPF neighbor {self.neighbor_ip} is {'full' if neighbor_up else 'down'}",
                "output": output
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}


class ReachabilityValidator(BaseValidator):
    """Reachability Test (Ping)"""
    
    def __init__(self, hostname: str, target_ip: str):
        super().__init__(hostname)
        self.target_ip = target_ip
    
    def validate(self) -> Dict[str, Any]:
        """Validate reachability via ping"""
        try:
            command = f"ping {self.target_ip} count 4"
            output = ssh_service.execute_command(self.hostname, command)
            
            success_rate = 100 if "100% packet loss" not in output else 0
            reachable = success_rate > 0
            return {
                "passed": reachable,
                "message": f"Ping to {self.target_ip} {'successful' if reachable else 'failed'}",
                "output": output,
                "success_rate": success_rate
            }
        except Exception as e:
            return {"passed": False, "message": str(e), "output": ""}
