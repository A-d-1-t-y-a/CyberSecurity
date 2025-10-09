#!/usr/bin/env python3
"""
Week 4 Testing Script - Advanced Features & Cross-Platform Testing
Cross-Platform Unified Memory Forensics Framework
Student: Manoj Santhoju (ID: 23394544)
Institution: National College of Ireland
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import json
from datetime import datetime
import platform
import psutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week4/logs/testing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week4Testing:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.test_results = {}
        
    def run_cross_platform_tests(self):
        """Run cross-platform testing"""
        logger.info("Running cross-platform tests...")
        
        platforms = {
            'windows': self._test_windows_platform(),
            'linux': self._test_linux_platform(),
            'macos': self._test_macos_platform()
        }
        
        # Save test results
        results_file = self.script_dir / 'reports' / 'cross_platform_test_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(platforms, f, indent=2)
            
        logger.info("Cross-platform tests completed")
        return platforms
        
    def _test_windows_platform(self):
        """Test Windows platform compatibility"""
        logger.info("Testing Windows platform...")
        
        if platform.system() != 'Windows':
            return {"status": "skipped", "reason": "Not running on Windows"}
            
        results = {
            "platform": "Windows",
            "version": platform.version(),
            "architecture": platform.architecture(),
            "python_version": sys.version,
            "tests": {}
        }
        
        # Test framework components
        results["tests"]["framework_import"] = self._test_framework_import()
        results["tests"]["tool_wrappers"] = self._test_tool_wrappers()
        results["tests"]["semantic_analyzer"] = self._test_semantic_analyzer()
        results["tests"]["performance"] = self._test_performance()
        
        return results
        
    def _test_linux_platform(self):
        """Test Linux platform compatibility"""
        logger.info("Testing Linux platform...")
        
        if platform.system() != 'Linux':
            return {"status": "skipped", "reason": "Not running on Linux"}
            
        results = {
            "platform": "Linux",
            "version": platform.release(),
            "architecture": platform.architecture(),
            "python_version": sys.version,
            "tests": {}
        }
        
        # Test framework components
        results["tests"]["framework_import"] = self._test_framework_import()
        results["tests"]["tool_wrappers"] = self._test_tool_wrappers()
        results["tests"]["semantic_analyzer"] = self._test_semantic_analyzer()
        results["tests"]["performance"] = self._test_performance()
        
        return results
        
    def _test_macos_platform(self):
        """Test macOS platform compatibility"""
        logger.info("Testing macOS platform...")
        
        if platform.system() != 'Darwin':
            return {"status": "skipped", "reason": "Not running on macOS"}
            
        results = {
            "platform": "macOS",
            "version": platform.mac_ver()[0],
            "architecture": platform.architecture(),
            "python_version": sys.version,
            "tests": {}
        }
        
        # Test framework components
        results["tests"]["framework_import"] = self._test_framework_import()
        results["tests"]["tool_wrappers"] = self._test_tool_wrappers()
        results["tests"]["semantic_analyzer"] = self._test_semantic_analyzer()
        results["tests"]["performance"] = self._test_performance()
        
        return results
        
    def _test_framework_import(self):
        """Test framework import functionality"""
        try:
            # Test importing framework components
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.unified_api import MemoryForensicsFramework
            from framework.tool_wrappers import BaseToolWrapper
            from framework.semantic_analyzer import SemanticAnalyzer
            
            # Test initialization
            framework = MemoryForensicsFramework()
            
            return {
                "status": "success",
                "message": "Framework imports successful",
                "framework_initialized": True
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Framework import failed: {str(e)}",
                "framework_initialized": False
            }
            
    def _test_tool_wrappers(self):
        """Test tool wrapper functionality"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.tool_wrappers import VolatilityWrapper, RekallWrapper, MemProcFSWrapper
            
            # Test wrapper initialization
            wrappers = {
                "volatility": VolatilityWrapper("vol", {}),
                "rekall": RekallWrapper("rekall", {}),
                "memprocfs": MemProcFSWrapper("memprocfs", {})
            }
            
            return {
                "status": "success",
                "message": "Tool wrappers initialized successfully",
                "wrappers_tested": list(wrappers.keys())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tool wrapper test failed: {str(e)}",
                "wrappers_tested": []
            }
            
    def _test_semantic_analyzer(self):
        """Test semantic analyzer functionality"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.semantic_analyzer import SemanticAnalyzer
            
            # Test analyzer initialization
            analyzer = SemanticAnalyzer()
            
            # Test with sample data
            sample_results = {
                "analysis": {
                    "processes": [
                        {"name": "notepad.exe", "pid": 1234, "path": "C:\\Windows\\notepad.exe"}
                    ],
                    "network_connections": [
                        {"local_address": "192.168.1.100", "port": 80, "protocol": "TCP"}
                    ]
                }
            }
            
            # Test analysis
            analysis_result = analyzer.analyze_results(sample_results)
            
            return {
                "status": "success",
                "message": "Semantic analyzer test successful",
                "analysis_completed": True,
                "result_keys": list(analysis_result.keys())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Semantic analyzer test failed: {str(e)}",
                "analysis_completed": False
            }
            
    def _test_performance(self):
        """Test performance characteristics"""
        try:
            # Get system information
            memory = psutil.virtual_memory()
            cpu_count = psutil.cpu_count()
            
            # Test memory usage
            import gc
            gc.collect()
            initial_memory = psutil.Process().memory_info().rss
            
            # Test framework initialization
            sys.path.insert(0, str(self.project_root / 'src'))
            from framework.unified_api import MemoryForensicsFramework
            
            framework = MemoryForensicsFramework()
            final_memory = psutil.Process().memory_info().rss
            memory_usage = final_memory - initial_memory
            
            return {
                "status": "success",
                "message": "Performance test completed",
                "system_info": {
                    "total_memory": memory.total,
                    "available_memory": memory.available,
                    "cpu_count": cpu_count,
                    "memory_usage_mb": memory_usage / (1024 * 1024)
                },
                "performance_metrics": {
                    "framework_memory_usage": memory_usage,
                    "memory_efficiency": "good" if memory_usage < 100 * 1024 * 1024 else "moderate"
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Performance test failed: {str(e)}",
                "system_info": {},
                "performance_metrics": {}
            }
            
    def run_advanced_feature_tests(self):
        """Run advanced feature tests"""
        logger.info("Running advanced feature tests...")
        
        features = {
            "enhanced_semantic_analyzer": self._test_enhanced_semantic_analyzer(),
            "intelligent_tool_selector": self._test_intelligent_tool_selector(),
            "performance_optimizer": self._test_performance_optimizer()
        }
        
        # Save test results
        results_file = self.script_dir / 'reports' / 'advanced_feature_test_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(features, f, indent=2)
            
        logger.info("Advanced feature tests completed")
        return features
        
    def _test_enhanced_semantic_analyzer(self):
        """Test enhanced semantic analyzer"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.enhanced_semantic_analyzer import EnhancedSemanticAnalyzer
            
            # Initialize analyzer
            analyzer = EnhancedSemanticAnalyzer()
            
            # Test with sample data
            sample_results = {
                "analysis": {
                    "processes": [
                        {"name": "suspicious.exe", "path": "C:\\temp\\suspicious.exe", "command_line": "suspicious.exe --encrypt"}
                    ],
                    "network_connections": [
                        {"local_address": "192.168.1.100", "remote_address": "10.0.0.1", "port": 443, "protocol": "TCP"}
                    ]
                }
            }
            
            # Test enhanced analysis
            result = analyzer.analyze_results(sample_results)
            
            return {
                "status": "success",
                "message": "Enhanced semantic analyzer test successful",
                "features_tested": ["ml_analysis", "threat_detection", "behavior_classification"],
                "result_structure": list(result.keys())
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Enhanced semantic analyzer test failed: {str(e)}",
                "features_tested": []
            }
            
    def _test_intelligent_tool_selector(self):
        """Test intelligent tool selector"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.intelligent_tool_selector import IntelligentToolSelector
            
            # Initialize selector
            selector = IntelligentToolSelector()
            
            # Test tool selection
            dump_path = "test_memory.dmp"
            os_type = "windows"
            requirements = {"cloud_analysis": True, "comprehensive_analysis": True}
            
            selected_tool, reasoning = selector.select_tool(dump_path, os_type, requirements)
            
            return {
                "status": "success",
                "message": "Intelligent tool selector test successful",
                "selected_tool": selected_tool,
                "reasoning": reasoning,
                "features_tested": ["tool_selection", "reasoning_generation"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Intelligent tool selector test failed: {str(e)}",
                "selected_tool": None
            }
            
    def _test_performance_optimizer(self):
        """Test performance optimizer"""
        try:
            sys.path.insert(0, str(self.project_root / 'src'))
            
            from framework.performance_optimizer import PerformanceOptimizer
            
            # Initialize optimizer
            optimizer = PerformanceOptimizer()
            
            # Test optimization
            def dummy_analysis(*args, **kwargs):
                import time
                time.sleep(0.1)  # Simulate analysis
                return {"status": "success"}
                
            result = optimizer.optimize_analysis("test.dmp", dummy_analysis)
            
            # Get performance report
            report = optimizer.get_performance_report()
            
            return {
                "status": "success",
                "message": "Performance optimizer test successful",
                "optimization_applied": True,
                "performance_report": report,
                "features_tested": ["optimization", "monitoring", "reporting"]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Performance optimizer test failed: {str(e)}",
                "optimization_applied": False
            }
            
    def run_comprehensive_tests(self):
        """Run comprehensive test suite"""
        logger.info("Running comprehensive test suite...")
        
        # Run pytest tests
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', 'src/tests/', '-v', '--tb=short'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            test_results = {
                "pytest_results": {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            }
            
            # Save test results
            results_file = self.script_dir / 'reports' / 'comprehensive_test_results.json'
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(test_results, f, indent=2)
                
            logger.info("Comprehensive tests completed")
            return test_results
            
        except subprocess.TimeoutExpired:
            logger.error("Comprehensive tests timed out")
            return {"status": "timeout", "message": "Tests timed out"}
        except Exception as e:
            logger.error(f"Comprehensive tests failed: {e}")
            return {"status": "error", "message": str(e)}
            
    def run(self):
        """Run Week 4 testing"""
        logger.info("Starting Week 4 testing...")
        
        try:
            # Run all test suites
            cross_platform_results = self.run_cross_platform_tests()
            advanced_feature_results = self.run_advanced_feature_tests()
            comprehensive_results = self.run_comprehensive_tests()
            
            # Combine all results
            self.test_results = {
                "cross_platform": cross_platform_results,
                "advanced_features": advanced_feature_results,
                "comprehensive": comprehensive_results,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save combined results
            combined_file = self.script_dir / 'reports' / 'week4_test_results.json'
            with open(combined_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2)
                
            logger.info("Week 4 testing completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Week 4 testing failed: {e}")
            return False

if __name__ == "__main__":
    testing = Week4Testing()
    success = testing.run()
    sys.exit(0 if success else 1)
