"""
Test Suite for Memory Forensics Framework
"""

import pytest
import tempfile
import os
from pathlib import Path
import json

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.unified_api import MemoryForensicsFramework
from framework.tool_wrappers import ToolWrapper
from framework.semantic_analyzer import SemanticAnalyzer
from framework.cloud_handler import CloudHandler

class TestMemoryForensicsFramework:
    """Test cases for the main framework"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.framework = MemoryForensicsFramework()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_framework_initialization(self):
        """Test framework initialization"""
        assert self.framework.name == "Unified Memory Forensics Framework"
        assert self.framework.version == "1.0.0"
        assert isinstance(self.framework.available_tools, dict)
    
    def test_framework_info(self):
        """Test framework info retrieval"""
        info = self.framework.get_framework_info()
        assert "name" in info
        assert "version" in info
        assert "platform" in info
        assert "available_tools" in info
    
    def test_os_detection(self):
        """Test OS detection functionality"""
        # Create a dummy memory dump file
        dummy_dump = os.path.join(self.temp_dir, "test.dmp")
        with open(dummy_dump, 'w') as f:
            f.write("dummy memory dump content")
        
        # Test OS detection
        os_type = self.framework.detect_os(dummy_dump)
        assert os_type in ["windows", "linux", "macos"]
    
    def test_tool_selection(self):
        """Test tool selection logic"""
        # Test tool selection for different OS types
        windows_tool = self.framework.select_tool("windows", "process")
        linux_tool = self.framework.select_tool("linux", "process")
        macos_tool = self.framework.select_tool("macos", "process")
        
        assert windows_tool in ["volatility", "rekall", "memprocfs"]
        assert linux_tool in ["volatility", "rekall"]
        assert macos_tool in ["rekall", "volatility"]
    
    def test_analysis_with_dummy_dump(self):
        """Test analysis with dummy memory dump"""
        # Create a dummy memory dump file
        dummy_dump = os.path.join(self.temp_dir, "test.dmp")
        with open(dummy_dump, 'w') as f:
            f.write("dummy memory dump content")
        
        # Test analysis (should handle gracefully even with dummy data)
        result = self.framework.analyze_memory_dump(dummy_dump, os_type="windows")
        
        assert "status" in result
        assert "memory_dump" in result
        assert "os_type" in result
        assert "tool_used" in result
    
    def test_export_results(self):
        """Test results export functionality"""
        # Create dummy results
        results = {
            "status": "success",
            "memory_dump": "test.dmp",
            "os_type": "windows",
            "tool_used": "volatility",
            "analysis_results": {"test": "data"}
        }
        
        # Test JSON export
        output_path = os.path.join(self.temp_dir, "results.json")
        success = self.framework.export_results(results, output_path, "json")
        
        assert success
        assert os.path.exists(output_path)
        
        # Verify content
        with open(output_path, 'r') as f:
            exported_data = json.load(f)
        assert exported_data["status"] == "success"

class TestToolWrapper:
    """Test cases for tool wrapper"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.tool_wrapper = ToolWrapper()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.tool_wrapper.cleanup()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_tool_wrapper_initialization(self):
        """Test tool wrapper initialization"""
        assert hasattr(self.tool_wrapper, 'tool_configs')
        assert "volatility" in self.tool_wrapper.tool_configs
        assert "rekall" in self.tool_wrapper.tool_configs
        assert "memprocfs" in self.tool_wrapper.tool_configs
    
    def test_get_plugins(self):
        """Test plugin retrieval"""
        volatility_plugins = self.tool_wrapper.get_plugins("volatility")
        rekall_plugins = self.tool_wrapper.get_plugins("rekall")
        memprocfs_plugins = self.tool_wrapper.get_plugins("memprocfs")
        
        assert isinstance(volatility_plugins, list)
        assert isinstance(rekall_plugins, list)
        assert isinstance(memprocfs_plugins, list)
        assert len(volatility_plugins) > 0
        assert len(rekall_plugins) > 0
        assert len(memprocfs_plugins) > 0
    
    def test_analyze_dump_with_dummy_data(self):
        """Test dump analysis with dummy data"""
        # Create dummy memory dump
        dummy_dump = os.path.join(self.temp_dir, "test.dmp")
        with open(dummy_dump, 'w') as f:
            f.write("dummy memory dump content")
        
        # Test analysis with each tool (should handle gracefully)
        for tool in ["volatility", "rekall", "memprocfs"]:
            try:
                result = self.tool_wrapper.analyze_dump(dummy_dump, tool, "process")
                assert "tool" in result
                assert "analysis_type" in result
                assert "plugins" in result
            except Exception as e:
                # Expected for dummy data
                assert "error" in str(e).lower() or "not found" in str(e).lower()

class TestSemanticAnalyzer:
    """Test cases for semantic analyzer"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.analyzer = SemanticAnalyzer()
    
    def test_semantic_analyzer_initialization(self):
        """Test semantic analyzer initialization"""
        assert hasattr(self.analyzer, 'semantic_patterns')
        assert hasattr(self.analyzer, 'scoring_weights')
        assert "processes" in self.analyzer.semantic_patterns
        assert "network" in self.analyzer.semantic_patterns
        assert "files" in self.analyzer.semantic_patterns
    
    def test_analyze_dummy_results(self):
        """Test semantic analysis with dummy results"""
        dummy_results = {
            "plugins": {
                "pslist": {
                    "status": "success",
                    "output": "Process 1: explorer.exe\nProcess 2: notepad.exe"
                },
                "netscan": {
                    "status": "success",
                    "output": "Connection: 192.168.1.1:80\nConnection: 10.0.0.1:443"
                }
            },
            "metadata": {
                "imageinfo": "Windows 10 x64"
            }
        }
        
        result = self.analyzer.analyze(dummy_results, "windows")
        
        assert "semantic_analysis" in result
        assert "categories" in result
        assert "threat_indicators" in result
        assert "semantic_score" in result
        assert "confidence" in result
        assert "recommendations" in result
    
    def test_get_info(self):
        """Test analyzer info retrieval"""
        info = self.analyzer.get_info()
        assert "name" in info
        assert "version" in info
        assert "categories" in info
        assert "scoring_weights" in info

class TestCloudHandler:
    """Test cases for cloud handler"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.cloud_handler = CloudHandler()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        self.cloud_handler.cleanup()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_cloud_handler_initialization(self):
        """Test cloud handler initialization"""
        assert hasattr(self.cloud_handler, 'temp_dir')
        assert hasattr(self.cloud_handler, 'aws_client')
        assert hasattr(self.cloud_handler, 'azure_client')
        assert hasattr(self.cloud_handler, 'gcp_client')
    
    def test_get_info(self):
        """Test cloud handler info retrieval"""
        info = self.cloud_handler.get_info()
        assert "name" in info
        assert "version" in info
        assert "temp_dir" in info
        assert "aws_available" in info
        assert "azure_available" in info
        assert "gcp_available" in info
    
    def test_unsupported_cloud_source(self):
        """Test handling of unsupported cloud sources"""
        with pytest.raises(ValueError):
            self.cloud_handler.download_dump("test.dmp", "unsupported")

# Integration tests
class TestIntegration:
    """Integration tests for the framework"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.framework = MemoryForensicsFramework()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_analysis(self):
        """Test end-to-end analysis workflow"""
        # Create dummy memory dump
        dummy_dump = os.path.join(self.temp_dir, "test.dmp")
        with open(dummy_dump, 'w') as f:
            f.write("dummy memory dump content")
        
        # Run analysis
        result = self.framework.analyze_memory_dump(
            dummy_dump, 
            os_type="windows",
            use_semantic=True
        )
        
        # Verify result structure
        assert "status" in result
        assert "memory_dump" in result
        assert "os_type" in result
        assert "tool_used" in result
        assert "analysis_results" in result
        
        # If analysis succeeded, check for semantic analysis
        if result["status"] == "success":
            analysis_results = result["analysis_results"]
            if "semantic_analysis" in analysis_results:
                semantic = analysis_results["semantic_analysis"]
                assert "semantic_score" in semantic
                assert "threat_indicators" in semantic
                assert "recommendations" in semantic

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
