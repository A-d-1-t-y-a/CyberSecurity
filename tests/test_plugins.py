import pytest
from unified_forensics.plugins.malware_detector import MalwareDetectorPlugin
from unified_forensics.plugins.network_analyzer import NetworkAnalyzerPlugin

class TestMalwareDetectorPlugin:
    def setup_method(self):
        self.plugin = MalwareDetectorPlugin()
    
    def test_plugin_initialization(self):
        assert self.plugin is not None
        assert hasattr(self.plugin, 'malware_patterns')
        assert hasattr(self.plugin, 'suspicious_strings')
    
    def test_analyze_empty_data(self):
        result = self.plugin.analyze({})
        
        assert 'malware_indicators' in result
        assert 'suspicious_processes' in result
        assert 'suspicious_artifacts' in result
        assert 'confidence_score' in result
        assert 'threat_level' in result
    
    def test_analyze_with_processes(self):
        data = {
            'processes': [
                {'name': 'cmd.exe', 'command_line': 'cmd /c echo test'},
                {'name': 'notepad.exe', 'command_line': 'notepad test.txt'}
            ]
        }
        
        result = self.plugin.analyze(data)
        
        assert len(result['malware_indicators']) > 0
        assert len(result['suspicious_processes']) > 0
        assert result['confidence_score'] > 0
    
    def test_analyze_with_artifacts(self):
        data = {
            'artifacts': [
                {'type': 'malfind', 'description': 'Code injection detected'}
            ]
        }
        
        result = self.plugin.analyze(data)
        
        assert len(result['suspicious_artifacts']) > 0
        assert result['confidence_score'] > 0
    
    def test_get_suspicious_reasons(self):
        reasons = self.plugin._get_suspicious_reasons('temp.exe', 'powershell -enc base64')
        
        assert 'Temporary location' in reasons
        assert 'PowerShell usage' in reasons
        assert 'Base64 encoding' in reasons
    
    def test_calculate_confidence_score(self):
        results = {
            'malware_indicators': [{'type': 'test'}],
            'suspicious_processes': [{'pid': 1}],
            'suspicious_artifacts': [{'type': 'test'}]
        }
        
        score = self.plugin._calculate_confidence_score(results)
        assert 0 <= score <= 1
    
    def test_determine_threat_level(self):
        assert self.plugin._determine_threat_level(0.9) == 'high'
        assert self.plugin._determine_threat_level(0.6) == 'medium'
        assert self.plugin._determine_threat_level(0.3) == 'low'

class TestNetworkAnalyzerPlugin:
    def setup_method(self):
        self.plugin = NetworkAnalyzerPlugin()
    
    def test_plugin_initialization(self):
        assert self.plugin is not None
        assert hasattr(self.plugin, 'suspicious_ports')
        assert hasattr(self.plugin, 'suspicious_ips')
        assert hasattr(self.plugin, 'malicious_domains')
    
    def test_analyze_empty_data(self):
        result = self.plugin.analyze({})
        
        assert 'network_connections' in result
        assert 'suspicious_connections' in result
        assert 'external_connections' in result
        assert 'internal_connections' in result
        assert 'port_analysis' in result
        assert 'ip_analysis' in result
        assert 'threat_indicators' in result
    
    def test_analyze_with_connections(self):
        data = {
            'network_connections': [
                {
                    'local_address': '127.0.0.1',
                    'local_port': 8080,
                    'remote_address': '192.168.1.1',
                    'remote_port': 80,
                    'protocol': 'tcp',
                    'state': 'ESTABLISHED'
                }
            ]
        }
        
        result = self.plugin.analyze(data)
        
        assert len(result['network_connections']) == 1
        assert len(result['external_connections']) == 1
        assert len(result['internal_connections']) == 0
    
    def test_analyze_suspicious_connections(self):
        data = {
            'network_connections': [
                {
                    'local_address': '127.0.0.1',
                    'local_port': 8080,
                    'remote_address': '192.168.1.1',
                    'remote_port': 22,
                    'protocol': 'tcp',
                    'state': 'ESTABLISHED'
                }
            ]
        }
        
        result = self.plugin.analyze(data)
        
        assert len(result['suspicious_connections']) > 0
        assert result['suspicious_connections'][0]['reason'] == 'Suspicious port 22'
    
    def test_analyze_ports(self):
        data = {
            'network_connections': [
                {'remote_port': 80},
                {'remote_port': 443},
                {'remote_port': 22}
            ]
        }
        
        result = self.plugin.analyze(data)
        port_analysis = result['port_analysis']
        
        assert port_analysis['total_unique_ports'] == 3
        assert 22 in port_analysis['suspicious_ports']
    
    def test_analyze_ips(self):
        data = {
            'network_connections': [
                {'remote_address': '192.168.1.1'},
                {'remote_address': '8.8.8.8'},
                {'remote_address': '127.0.0.1'}
            ]
        }
        
        result = self.plugin.analyze(data)
        ip_analysis = result['ip_analysis']
        
        assert ip_analysis['unique_ip_count'] == 3
        assert '192.168.1.1' in ip_analysis['internal_ips']
        assert '8.8.8.8' in ip_analysis['external_ips']
    
    def test_is_internal_ip(self):
        assert self.plugin._is_internal_ip('192.168.1.1') == True
        assert self.plugin._is_internal_ip('127.0.0.1') == True
        assert self.plugin._is_internal_ip('8.8.8.8') == False
        assert self.plugin._is_internal_ip('10.0.0.1') == True
    
    def test_is_malicious_domain(self):
        assert self.plugin._is_malicious_domain('malware.com') == True
        assert self.plugin._is_malicious_domain('google.com') == False
        assert self.plugin._is_malicious_domain('suspicious.org') == True
    
    def test_ip_in_range(self):
        assert self.plugin._ip_in_range('192.168.1.1', '192.168.0.0/16') == True
        assert self.plugin._ip_in_range('8.8.8.8', '192.168.0.0/16') == False
        assert self.plugin._ip_in_range('127.0.0.1', '127.0.0.1') == True
