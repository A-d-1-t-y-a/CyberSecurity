import subprocess
import json
import logging
import os
from typing import Dict, Any, List

class RekallWrapper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rekall_cmd = self._find_rekall_cmd()
        self.available = self._check_availability()
    
    def _find_rekall_cmd(self) -> str:
        possible_paths = [
            'rekall',
            'python -m rekall',
            'rekall-core'
        ]
        
        for cmd in possible_paths:
            try:
                result = subprocess.run([cmd, '--help'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    return cmd
            except:
                continue
        
        return 'rekall'
    
    def _check_availability(self) -> bool:
        try:
            result = subprocess.run([self.rekall_cmd, '--help'], 
                                  capture_output=True, text=True, timeout=5, shell=True)
            return result.returncode == 0
        except:
            return False
    
    def analyze(self, memory_dump_path: str, os_type: str) -> Dict[str, Any]:
        if not self.available:
            self.logger.warning("Rekall is not available, returning empty results")
            return {
                'processes': [],
                'network': [],
                'modules': [],
                'memory_regions': [],
                'artifacts': []
            }
        results = {
            'processes': [],
            'network': [],
            'modules': [],
            'memory_regions': [],
            'artifacts': []
        }
        
        try:
            results['processes'] = self._get_processes(memory_dump_path, os_type)
            results['network'] = self._get_network_connections(memory_dump_path, os_type)
            results['modules'] = self._get_kernel_modules(memory_dump_path, os_type)
            results['memory_regions'] = self._get_memory_regions(memory_dump_path, os_type)
            results['artifacts'] = self._get_artifacts(memory_dump_path, os_type)
            
        except Exception as e:
            self.logger.error(f"Rekall analysis failed: {str(e)}")
            raise
        
        return results
    
    def _get_processes(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        try:
            if os_type.lower() == 'windows':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'pslist', '--format', 'json']
            elif os_type.lower() == 'linux':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'pslist', '--format', 'json']
            else:
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'pslist', '--format', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return self._parse_text_output(result.stdout, 'processes')
                
        except Exception as e:
            self.logger.warning(f"Process extraction failed: {str(e)}")
            return []
    
    def _get_network_connections(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        try:
            if os_type.lower() == 'windows':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'netscan', '--format', 'json']
            elif os_type.lower() == 'linux':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'netstat', '--format', 'json']
            else:
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'netstat', '--format', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return self._parse_text_output(result.stdout, 'network')
                
        except Exception as e:
            self.logger.warning(f"Network extraction failed: {str(e)}")
            return []
    
    def _get_kernel_modules(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        try:
            if os_type.lower() == 'windows':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'modules', '--format', 'json']
            elif os_type.lower() == 'linux':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'lsmod', '--format', 'json']
            else:
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'lsmod', '--format', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return self._parse_text_output(result.stdout, 'modules')
                
        except Exception as e:
            self.logger.warning(f"Module extraction failed: {str(e)}")
            return []
    
    def _get_memory_regions(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        try:
            if os_type.lower() == 'windows':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'vad', '--format', 'json']
            elif os_type.lower() == 'linux':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'proc', '--format', 'json']
            else:
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'proc', '--format', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return self._parse_text_output(result.stdout, 'memory_regions')
                
        except Exception as e:
            self.logger.warning(f"Memory region extraction failed: {str(e)}")
            return []
    
    def _get_artifacts(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        artifacts = []
        
        try:
            if os_type.lower() == 'windows':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'malfind', '--format', 'json']
            elif os_type.lower() == 'linux':
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'malfind', '--format', 'json']
            else:
                cmd = [self.rekall_cmd, '-f', memory_dump_path, 'malfind', '--format', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                artifacts.extend(json.loads(result.stdout))
            else:
                artifacts.extend(self._parse_text_output(result.stdout, 'artifacts'))
                
        except Exception as e:
            self.logger.warning(f"Artifact extraction failed: {str(e)}")
        
        return artifacts
    
    def _parse_text_output(self, output: str, data_type: str) -> List[Dict]:
        if data_type == 'processes':
            return self._parse_processes_text(output)
        elif data_type == 'network':
            return self._parse_network_text(output)
        elif data_type == 'modules':
            return self._parse_modules_text(output)
        elif data_type == 'memory_regions':
            return self._parse_memory_regions_text(output)
        elif data_type == 'artifacts':
            return self._parse_artifacts_text(output)
        else:
            return []
    
    def _parse_processes_text(self, output: str) -> List[Dict]:
        processes = []
        lines = output.strip().split('\n')
        
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    processes.append({
                        'pid': int(parts[0]) if parts[0].isdigit() else 0,
                        'name': parts[1],
                        'parent_pid': int(parts[2]) if parts[2].isdigit() else 0,
                        'command_line': ' '.join(parts[3:]) if len(parts) > 3 else ''
                    })
        
        return processes
    
    def _parse_network_text(self, output: str) -> List[Dict]:
        connections = []
        lines = output.strip().split('\n')
        
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    connections.append({
                        'local_address': parts[0],
                        'local_port': int(parts[1]) if parts[1].isdigit() else 0,
                        'remote_address': parts[2],
                        'remote_port': int(parts[3]) if parts[3].isdigit() else 0,
                        'protocol': parts[4] if len(parts) > 4 else 'tcp',
                        'state': parts[5] if len(parts) > 5 else 'unknown'
                    })
        
        return connections
    
    def _parse_modules_text(self, output: str) -> List[Dict]:
        modules = []
        lines = output.strip().split('\n')
        
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    modules.append({
                        'name': parts[0],
                        'base_address': parts[1],
                        'size': int(parts[2]) if parts[2].isdigit() else 0,
                        'path': ' '.join(parts[3:]) if len(parts) > 3 else ''
                    })
        
        return modules
    
    def _parse_memory_regions_text(self, output: str) -> List[Dict]:
        regions = []
        lines = output.strip().split('\n')
        
        for line in lines[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    regions.append({
                        'start_address': parts[0],
                        'end_address': parts[1],
                        'size': int(parts[2]) if parts[2].isdigit() else 0,
                        'protection': parts[3] if len(parts) > 3 else 'unknown',
                        'type': parts[4] if len(parts) > 4 else 'unknown'
                    })
        
        return regions
    
    def _parse_artifacts_text(self, output: str) -> List[Dict]:
        artifacts = []
        lines = output.strip().split('\n')
        
        for line in lines[1:]:
            if line.strip():
                artifacts.append({
                    'type': 'malfind',
                    'description': line,
                    'location': 'memory',
                    'confidence': 0.5,
                    'severity': 'medium'
                })
        
        return artifacts
