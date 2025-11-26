import subprocess
import json
import logging
import os
import platform
from typing import Dict, Any, List

class VolatilityWrapper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.volatility_cmd = self._find_volatility_cmd()
        self.use_shell = platform.system() == 'Windows'
    
    def _find_volatility_cmd(self) -> str:
        possible_paths = [
            'vol.py',
            'volatility3',
            'vol',
            'python -m volatility3'
        ]
        
        use_shell = platform.system() == 'Windows'
        for cmd in possible_paths:
            try:
                if 'python -m' in cmd:
                    result = subprocess.run(['python', '-m', 'volatility3', '--help'], 
                                          capture_output=True, text=True, timeout=10, shell=use_shell)
                else:
                    result = subprocess.run([cmd, '--help'], 
                                          capture_output=True, text=True, timeout=10, shell=use_shell)
                
                if result.returncode == 0:
                    return cmd
            except:
                continue
        
        # If no command found, use python -m volatility3 as fallback
        return 'python -m volatility3'
    
    def analyze(self, memory_dump_path: str, os_type: str) -> Dict[str, Any]:
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
            self.logger.error(f"Volatility analysis failed: {str(e)}")
            raise
        
        return results
    
    def _get_processes(self, memory_dump_path: str, os_type: str) -> List[Dict]:
        try:
            if os_type.lower() == 'windows':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'windows.pslist', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'windows.pslist', '--output', 'json']
            elif os_type.lower() == 'linux':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'linux.pslist', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'linux.pslist', '--output', 'json']
            else:
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'mac.pslist', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'mac.pslist', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=self.use_shell)
            
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
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'windows.netscan', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'windows.netscan', '--output', 'json']
            elif os_type.lower() == 'linux':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'linux.netstat', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'linux.netstat', '--output', 'json']
            else:
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'mac.netstat', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'mac.netstat', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=self.use_shell)
            
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
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'windows.modules', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'windows.modules', '--output', 'json']
            elif os_type.lower() == 'linux':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'linux.lsmod', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'linux.lsmod', '--output', 'json']
            else:
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'mac.lsmod', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'mac.lsmod', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=self.use_shell)
            
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
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'windows.vadinfo', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'windows.vadinfo', '--output', 'json']
            elif os_type.lower() == 'linux':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'linux.proc', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'linux.proc', '--output', 'json']
            else:
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'mac.proc', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'mac.proc', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=self.use_shell)
            
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
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'windows.malfind', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'windows.malfind', '--output', 'json']
            elif os_type.lower() == 'linux':
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'linux.malfind', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'linux.malfind', '--output', 'json']
            else:
                if 'python -m' in self.volatility_cmd:
                    cmd = ['python', '-m', 'volatility3', '-f', memory_dump_path, 'mac.malfind', '--output', 'json']
                else:
                    cmd = [self.volatility_cmd, '-f', memory_dump_path, 'mac.malfind', '--output', 'json']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, shell=self.use_shell)
            
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
