import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock

from unified_forensics.core.framework import UnifiedForensicsFramework
from unified_forensics.core.os_detector import OSDetector
from unified_forensics.core.output_standardizer import OutputStandardizer

class TestUnifiedForensicsFramework:
    def setup_method(self):
        self.framework = UnifiedForensicsFramework()
    
    def test_framework_initialization(self):
        assert self.framework is not None
        assert hasattr(self.framework, 'os_detector')
        assert hasattr(self.framework, 'output_standardizer')
        assert hasattr(self.framework, 'tools')
    
    def test_get_supported_os(self):
        supported_os = self.framework.get_supported_os()
        assert isinstance(supported_os, list)
        assert 'windows' in supported_os
        assert 'linux' in supported_os
        assert 'macos' in supported_os
    
    def test_get_available_tools(self):
        tools = self.framework.get_available_tools()
        assert isinstance(tools, list)
        assert 'volatility' in tools
        assert 'rekall' in tools
        assert 'memprocfs' in tools
    
    def test_get_available_plugins(self):
        plugins = self.framework.get_available_plugins()
        assert isinstance(plugins, list)
        assert 'malware_detector' in plugins
        assert 'network_analyzer' in plugins
    
    def test_select_tool(self):
        assert self.framework._select_tool('windows') == 'volatility'
        assert self.framework._select_tool('linux') == 'volatility'
        assert self.framework._select_tool('macos') == 'rekall'
        assert self.framework._select_tool('unknown') == 'volatility'
    
    @patch('unified_forensics.core.framework.os.path.exists')
    def test_analyze_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError):
            self.framework.analyze('nonexistent.mem')
    
    @patch('unified_forensics.core.framework.os.path.exists')
    @patch.object(UnifiedForensicsFramework, '_run_analysis')
    def test_analyze_success(self, mock_run_analysis, mock_exists):
        mock_exists.return_value = True
        mock_run_analysis.return_value = {
            'processes': [],
            'network': [],
            'modules': [],
            'memory_regions': [],
            'artifacts': []
        }
        
        result = self.framework.analyze('test.mem', os_type='windows')
        
        assert 'metadata' in result
        assert 'processes' in result
        assert 'network_connections' in result
        assert 'statistics' in result
    
    @patch('unified_forensics.core.framework.os.path.exists')
    @patch.object(UnifiedForensicsFramework, '_run_analysis')
    def test_analyze_with_plugins(self, mock_run_analysis, mock_exists):
        mock_exists.return_value = True
        mock_run_analysis.return_value = {
            'processes': [],
            'network': [],
            'modules': [],
            'memory_regions': [],
            'artifacts': []
        }
        
        result = self.framework.analyze('test.mem', os_type='windows', plugins=['malware_detector'])
        
        assert 'plugin_results' in result
        assert 'malware_detector' in result['plugin_results']
    
    @patch('unified_forensics.core.framework.os.path.exists')
    @patch.object(UnifiedForensicsFramework, '_run_analysis')
    def test_analyze_with_output_file(self, mock_run_analysis, mock_exists):
        mock_exists.return_value = True
        mock_run_analysis.return_value = {
            'processes': [],
            'network': [],
            'modules': [],
            'memory_regions': [],
            'artifacts': []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            output_file = f.name
        
        try:
            result = self.framework.analyze('test.mem', os_type='windows', output_file=output_file)
            
            assert os.path.exists(output_file)
            with open(output_file, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == result
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)

class TestOSDetector:
    def setup_method(self):
        self.detector = OSDetector()
    
    def test_detect_os_windows(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'Windows NTOSKRNL Microsoft')
            f.flush()
            
            os_type = self.detector.detect_os(f.name)
            assert os_type == 'windows'
        
        os.unlink(f.name)
    
    def test_detect_os_linux(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'Linux kernel vmlinux')
            f.flush()
            
            os_type = self.detector.detect_os(f.name)
            assert os_type == 'linux'
        
        os.unlink(f.name)
    
    def test_detect_os_macos(self):
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'Darwin XNU mach_kernel')
            f.flush()
            
            os_type = self.detector.detect_os(f.name)
            assert os_type == 'macos'
        
        os.unlink(f.name)
    
    def test_detect_os_by_filename(self):
        with tempfile.NamedTemporaryFile(suffix='_windows.mem', delete=False) as f:
            f.write(b'unknown data')
            f.flush()
            
            os_type = self.detector.detect_os(f.name)
            assert os_type == 'windows'
        
        os.unlink(f.name)

class TestOutputStandardizer:
    def setup_method(self):
        self.standardizer = OutputStandardizer()
    
    def test_standardize_empty_data(self):
        result = self.standardizer.standardize({}, 'windows')
        
        assert 'metadata' in result
        assert 'processes' in result
        assert 'network_connections' in result
        assert 'statistics' in result
        assert result['metadata']['os_type'] == 'windows'
    
    def test_standardize_processes(self):
        raw_data = {
            'processes': [
                {'pid': 1234, 'name': 'test.exe', 'parent_pid': 5678}
            ]
        }
        
        result = self.standardizer.standardize(raw_data, 'windows')
        
        assert len(result['processes']) == 1
        assert result['processes'][0]['pid'] == 1234
        assert result['processes'][0]['name'] == 'test.exe'
        assert result['processes'][0]['parent_pid'] == 5678
    
    def test_standardize_network(self):
        raw_data = {
            'network': [
                {'local_address': '127.0.0.1', 'local_port': 8080, 'remote_address': '192.168.1.1', 'remote_port': 80}
            ]
        }
        
        result = self.standardizer.standardize(raw_data, 'windows')
        
        assert len(result['network_connections']) == 1
        assert result['network_connections'][0]['local_address'] == '127.0.0.1'
        assert result['network_connections'][0]['local_port'] == 8080
    
    def test_calculate_statistics(self):
        raw_data = {
            'processes': [
                {'pid': 1, 'name': 'normal.exe'},
                {'pid': 2, 'name': 'suspicious.exe'}
            ],
            'network': [
                {'state': 'ESTABLISHED'},
                {'state': 'LISTENING'}
            ],
            'modules': [
                {'name': 'module1'},
                {'name': 'module2'}
            ]
        }
        
        result = self.standardizer.standardize(raw_data, 'windows')
        stats = result['statistics']
        
        assert stats['total_processes'] == 2
        assert stats['total_network_connections'] == 2
        assert stats['total_kernel_modules'] == 2
        assert stats['active_connections'] == 1
    
    def test_is_suspicious_process(self):
        standardizer = OutputStandardizer()
        
        suspicious_proc = {'name': 'cmd.exe'}
        normal_proc = {'name': 'notepad.exe'}
        
        assert standardizer._is_suspicious_process(suspicious_proc) == True
        assert standardizer._is_suspicious_process(normal_proc) == False
    
    def test_is_suspicious_module(self):
        standardizer = OutputStandardizer()
        
        suspicious_module = {'path': '/tmp/suspicious.dll'}
        normal_module = {'path': '/system/normal.dll'}
        
        assert standardizer._is_suspicious_module(suspicious_module) == True
        assert standardizer._is_suspicious_module(normal_module) == False
