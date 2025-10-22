import re
import logging
from typing import Dict, Any, List

class NetworkAnalyzerPlugin:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.suspicious_ports = [22, 23, 80, 443, 8080, 8443, 3389, 5900, 5901]
        self.suspicious_ips = [
            '10.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16',
            '127.0.0.1'
        ]
        self.malicious_domains = [
            'malware.com',
            'suspicious.org',
            'bad.net'
        ]
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        results = {
            'network_connections': [],
            'suspicious_connections': [],
            'external_connections': [],
            'internal_connections': [],
            'port_analysis': {},
            'ip_analysis': {},
            'threat_indicators': []
        }
        
        try:
            network_data = data.get('network_connections', [])
            results['network_connections'] = network_data
            results['suspicious_connections'] = self._analyze_suspicious_connections(network_data)
            results['external_connections'] = self._analyze_external_connections(network_data)
            results['internal_connections'] = self._analyze_internal_connections(network_data)
            results['port_analysis'] = self._analyze_ports(network_data)
            results['ip_analysis'] = self._analyze_ips(network_data)
            results['threat_indicators'] = self._detect_threat_indicators(network_data)
            
        except Exception as e:
            self.logger.error(f"Network analysis failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_suspicious_connections(self, connections: List[Dict]) -> List[Dict]:
        suspicious = []
        
        for conn in connections:
            remote_port = conn.get('remote_port', 0)
            remote_address = conn.get('remote_address', '')
            local_port = conn.get('local_port', 0)
            
            if remote_port in self.suspicious_ports:
                suspicious.append({
                    'connection': conn,
                    'reason': f'Suspicious port {remote_port}',
                    'severity': 'medium'
                })
            
            if self._is_suspicious_ip(remote_address):
                suspicious.append({
                    'connection': conn,
                    'reason': f'Suspicious IP {remote_address}',
                    'severity': 'high'
                })
            
            if self._is_malicious_domain(remote_address):
                suspicious.append({
                    'connection': conn,
                    'reason': f'Malicious domain {remote_address}',
                    'severity': 'high'
                })
        
        return suspicious
    
    def _analyze_external_connections(self, connections: List[Dict]) -> List[Dict]:
        external = []
        
        for conn in connections:
            remote_address = conn.get('remote_address', '')
            
            if not self._is_internal_ip(remote_address):
                external.append(conn)
        
        return external
    
    def _analyze_internal_connections(self, connections: List[Dict]) -> List[Dict]:
        internal = []
        
        for conn in connections:
            remote_address = conn.get('remote_address', '')
            
            if self._is_internal_ip(remote_address):
                internal.append(conn)
        
        return internal
    
    def _analyze_ports(self, connections: List[Dict]) -> Dict[str, Any]:
        port_usage = {}
        
        for conn in connections:
            port = conn.get('remote_port', 0)
            if port > 0:
                if port not in port_usage:
                    port_usage[port] = 0
                port_usage[port] += 1
        
        return {
            'most_used_ports': sorted(port_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            'suspicious_ports': [port for port in port_usage.keys() if port in self.suspicious_ports],
            'total_unique_ports': len(port_usage)
        }
    
    def _analyze_ips(self, connections: List[Dict]) -> Dict[str, Any]:
        ip_usage = {}
        
        for conn in connections:
            ip = conn.get('remote_address', '')
            if ip:
                if ip not in ip_usage:
                    ip_usage[ip] = 0
                ip_usage[ip] += 1
        
        return {
            'most_connected_ips': sorted(ip_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            'unique_ip_count': len(ip_usage),
            'internal_ips': [ip for ip in ip_usage.keys() if self._is_internal_ip(ip)],
            'external_ips': [ip for ip in ip_usage.keys() if not self._is_internal_ip(ip)]
        }
    
    def _detect_threat_indicators(self, connections: List[Dict]) -> List[Dict]:
        indicators = []
        
        for conn in connections:
            remote_address = conn.get('remote_address', '')
            remote_port = conn.get('remote_port', 0)
            state = conn.get('state', '')
            
            if state == 'LISTENING' and remote_port in [22, 23, 3389, 5900, 5901]:
                indicators.append({
                    'type': 'potential_backdoor',
                    'port': remote_port,
                    'address': remote_address,
                    'severity': 'high'
                })
            
            if self._is_malicious_domain(remote_address):
                indicators.append({
                    'type': 'malicious_domain',
                    'address': remote_address,
                    'severity': 'high'
                })
        
        return indicators
    
    def _is_suspicious_ip(self, ip: str) -> bool:
        for suspicious_ip in self.suspicious_ips:
            if self._ip_in_range(ip, suspicious_ip):
                return True
        return False
    
    def _is_internal_ip(self, ip: str) -> bool:
        internal_ranges = [
            '10.0.0.0/8',
            '172.16.0.0/12',
            '192.168.0.0/16',
            '127.0.0.0/8'
        ]
        
        for range_ip in internal_ranges:
            if self._ip_in_range(ip, range_ip):
                return True
        return False
    
    def _is_malicious_domain(self, address: str) -> bool:
        for domain in self.malicious_domains:
            if domain in address:
                return True
        return False
    
    def _ip_in_range(self, ip: str, range_ip: str) -> bool:
        try:
            if '/' in range_ip:
                network, prefix = range_ip.split('/')
                prefix = int(prefix)
                
                ip_parts = [int(x) for x in ip.split('.')]
                network_parts = [int(x) for x in network.split('.')]
                
                mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
                
                ip_int = (ip_parts[0] << 24) + (ip_parts[1] << 16) + (ip_parts[2] << 8) + ip_parts[3]
                network_int = (network_parts[0] << 24) + (network_parts[1] << 16) + (network_parts[2] << 8) + network_parts[3]
                
                return (ip_int & mask) == (network_int & mask)
            else:
                return ip == range_ip
        except:
            return False
