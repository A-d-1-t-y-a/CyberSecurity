import json
import logging
from typing import Dict, Any, List
from datetime import datetime

class OutputStandardizer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def standardize(self, raw_results: Dict[str, Any], os_type: str) -> Dict[str, Any]:
        standardized = {
            'metadata': {
                'os_type': os_type,
                'analysis_timestamp': datetime.now().isoformat(),
                'framework_version': '1.0.0'
            },
            'processes': self._standardize_processes(raw_results.get('processes', [])),
            'network_connections': self._standardize_network(raw_results.get('network', [])),
            'kernel_modules': self._standardize_modules(raw_results.get('modules', [])),
            'memory_regions': self._standardize_memory_regions(raw_results.get('memory_regions', [])),
            'artifacts': self._standardize_artifacts(raw_results.get('artifacts', [])),
            'statistics': self._calculate_statistics(raw_results)
        }
        
        return standardized
    
    def _standardize_processes(self, processes: List[Dict]) -> List[Dict]:
        standardized_processes = []
        
        for proc in processes:
            standardized_proc = {
                'pid': proc.get('pid', 0),
                'name': proc.get('name', 'unknown'),
                'parent_pid': proc.get('parent_pid', 0),
                'command_line': proc.get('command_line', ''),
                'start_time': proc.get('start_time', ''),
                'memory_usage': proc.get('memory_usage', 0),
                'threads': proc.get('threads', 0),
                'suspicious': self._is_suspicious_process(proc)
            }
            standardized_processes.append(standardized_proc)
        
        return standardized_processes
    
    def _standardize_network(self, network: List[Dict]) -> List[Dict]:
        standardized_network = []
        
        for conn in network:
            standardized_conn = {
                'local_address': conn.get('local_address', ''),
                'local_port': conn.get('local_port', 0),
                'remote_address': conn.get('remote_address', ''),
                'remote_port': conn.get('remote_port', 0),
                'protocol': conn.get('protocol', ''),
                'state': conn.get('state', ''),
                'pid': conn.get('pid', 0),
                'process_name': conn.get('process_name', '')
            }
            standardized_network.append(standardized_conn)
        
        return standardized_network
    
    def _standardize_modules(self, modules: List[Dict]) -> List[Dict]:
        standardized_modules = []
        
        for module in modules:
            standardized_module = {
                'name': module.get('name', ''),
                'base_address': module.get('base_address', ''),
                'size': module.get('size', 0),
                'path': module.get('path', ''),
                'suspicious': self._is_suspicious_module(module)
            }
            standardized_modules.append(standardized_module)
        
        return standardized_modules
    
    def _standardize_memory_regions(self, regions: List[Dict]) -> List[Dict]:
        standardized_regions = []
        
        for region in regions:
            standardized_region = {
                'start_address': region.get('start_address', ''),
                'end_address': region.get('end_address', ''),
                'size': region.get('size', 0),
                'protection': region.get('protection', ''),
                'type': region.get('type', ''),
                'suspicious': self._is_suspicious_region(region)
            }
            standardized_regions.append(standardized_region)
        
        return standardized_regions
    
    def _standardize_artifacts(self, artifacts: List[Dict]) -> List[Dict]:
        standardized_artifacts = []
        
        for artifact in artifacts:
            standardized_artifact = {
                'type': artifact.get('type', ''),
                'description': artifact.get('description', ''),
                'location': artifact.get('location', ''),
                'confidence': artifact.get('confidence', 0.0),
                'severity': artifact.get('severity', 'low')
            }
            standardized_artifacts.append(standardized_artifact)
        
        return standardized_artifacts
    
    def _calculate_statistics(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        processes = raw_results.get('processes', [])
        network = raw_results.get('network', [])
        modules = raw_results.get('modules', [])
        
        return {
            'total_processes': len(processes),
            'total_network_connections': len(network),
            'total_kernel_modules': len(modules),
            'suspicious_processes': len([p for p in processes if self._is_suspicious_process(p)]),
            'suspicious_modules': len([m for m in modules if self._is_suspicious_module(m)]),
            'active_connections': len([c for c in network if c.get('state') == 'ESTABLISHED'])
        }
    
    def _is_suspicious_process(self, process: Dict) -> bool:
        suspicious_names = [
            'cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe',
            'rundll32.exe', 'regsvr32.exe', 'mshta.exe'
        ]
        
        name = process.get('name', '').lower()
        return name in suspicious_names or 'temp' in name or 'tmp' in name
    
    def _is_suspicious_module(self, module: Dict) -> bool:
        suspicious_paths = ['temp', 'tmp', 'downloads', 'appdata']
        path = module.get('path', '').lower()
        return any(susp in path for susp in suspicious_paths)
    
    def _is_suspicious_region(self, region: Dict) -> bool:
        protection = region.get('protection', '').upper()
        return 'EXECUTE' in protection and 'WRITE' in protection
