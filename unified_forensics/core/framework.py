import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

from .os_detector import OSDetector
from .output_standardizer import OutputStandardizer
from .detection_metrics import DetectionMetricsCalculator
from ..tools.volatility_wrapper import VolatilityWrapper
from ..tools.rekall_wrapper import RekallWrapper
from ..tools.memprocfs_wrapper import MemProcFSWrapper

class UnifiedForensicsFramework:
    def __init__(self):
        self.os_detector = OSDetector()
        self.output_standardizer = OutputStandardizer()
        self.metrics_calculator = DetectionMetricsCalculator()
        self.tools = {
            'volatility': VolatilityWrapper(),
            'rekall': RekallWrapper(),
            'memprocfs': MemProcFSWrapper()
        }
        self.logger = logging.getLogger(__name__)
        
    def analyze(self, memory_dump_path: str, os_type: Optional[str] = None, 
                plugins: Optional[List[str]] = None, output_file: Optional[str] = None,
                enable_metrics: bool = False) -> Dict[str, Any]:
        
        if not os.path.exists(memory_dump_path):
            raise FileNotFoundError(f"Memory dump file not found: {memory_dump_path}")
        
        if os_type is None:
            os_type = self.os_detector.detect_os(memory_dump_path)
            self.logger.info(f"Detected OS: {os_type}")
        
        tool = self._select_tool(os_type)
        self.logger.info(f"Selected tool: {tool}")
        
        # Start metrics calculation if enabled
        if enable_metrics:
            self.metrics_calculator.start_analysis()
        
        raw_results = self._run_analysis(memory_dump_path, tool, os_type)
        
        standardized_results = self.output_standardizer.standardize(raw_results, os_type)
        
        if plugins:
            standardized_results = self._run_plugins(standardized_results, plugins)
        
        # Add detection metrics if enabled
        if enable_metrics:
            self.metrics_calculator.end_analysis()
            metrics = self.metrics_calculator.calculate_metrics()
            standardized_results['detection_metrics'] = metrics.__dict__
            standardized_results['detailed_metrics'] = self.metrics_calculator.get_detailed_metrics()
        
        if output_file:
            self._save_results(standardized_results, output_file)
        
        return standardized_results
    
    def _select_tool(self, os_type: str) -> str:
        tool_mapping = {
            'windows': 'volatility',
            'linux': 'volatility', 
            'macos': 'rekall'
        }
        return tool_mapping.get(os_type.lower(), 'volatility')
    
    def _run_analysis(self, memory_dump_path: str, tool: str, os_type: str) -> Dict[str, Any]:
        try:
            return self.tools[tool].analyze(memory_dump_path, os_type)
        except Exception as e:
            self.logger.error(f"Analysis failed with {tool}: {str(e)}")
            return self._fallback_analysis(memory_dump_path, os_type)
    
    def _fallback_analysis(self, memory_dump_path: str, os_type: str) -> Dict[str, Any]:
        fallback_tools = ['rekall', 'memprocfs'] if os_type.lower() != 'macos' else ['memprocfs']
        
        for tool in fallback_tools:
            try:
                self.logger.info(f"Trying fallback tool: {tool}")
                return self.tools[tool].analyze(memory_dump_path, os_type)
            except Exception as e:
                self.logger.warning(f"Fallback tool {tool} failed: {str(e)}")
                continue
        
        raise RuntimeError("All analysis tools failed")
    
    def _run_plugins(self, results: Dict[str, Any], plugins: List[str]) -> Dict[str, Any]:
        plugin_results = {}
        
        for plugin_name in plugins:
            try:
                if plugin_name == 'malware':
                    plugin_module = __import__('unified_forensics.plugins.malware_detector', fromlist=[''])
                    plugin_class = getattr(plugin_module, 'MalwareDetectorPlugin')
                elif plugin_name == 'network':
                    plugin_module = __import__('unified_forensics.plugins.network_analyzer', fromlist=[''])
                    plugin_class = getattr(plugin_module, 'NetworkAnalyzerPlugin')
                else:
                    plugin_module = __import__(f'unified_forensics.plugins.{plugin_name}', fromlist=[''])
                    plugin_class = getattr(plugin_module, f'{plugin_name.title().replace("_", "")}Plugin')
                
                plugin_instance = plugin_class()
                plugin_results[plugin_name] = plugin_instance.analyze(results)
            except Exception as e:
                self.logger.warning(f"Plugin {plugin_name} failed: {str(e)}")
                plugin_results[plugin_name] = {"error": str(e)}
        
        results['plugin_results'] = plugin_results
        return results
    
    def _save_results(self, results: Dict[str, Any], output_file: str) -> None:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        self.logger.info(f"Results saved to {output_file}")
    
    def get_supported_os(self) -> List[str]:
        return ['windows', 'linux', 'macos']
    
    def get_available_tools(self) -> List[str]:
        return list(self.tools.keys())
    
    def get_available_plugins(self) -> List[str]:
        plugins_dir = Path(__file__).parent.parent / 'plugins'
        return [f.stem for f in plugins_dir.glob('*.py') if f.stem != '__init__']
    
    def run_experimental_analysis(self, memory_dump_path: str, os_type: str, 
                                 event_rates: List[int] = None) -> Dict[str, Any]:
        """Run experimental analysis with detection metrics"""
        from .experimental_framework import ExperimentalFramework
        
        experimental_framework = ExperimentalFramework()
        return experimental_framework.run_detection_experiment(memory_dump_path, os_type, event_rates)
    
    def validate_cross_platform(self, test_dumps: Dict[str, str]) -> Dict[str, Any]:
        """Validate cross-platform functionality"""
        from .experimental_framework import ExperimentalFramework
        
        experimental_framework = ExperimentalFramework()
        return experimental_framework.run_cross_platform_validation(test_dumps)
    
    def get_detection_metrics(self) -> Dict[str, Any]:
        """Get current detection metrics"""
        return self.metrics_calculator.get_detailed_metrics()
    
    def reset_metrics(self):
        """Reset detection metrics"""
        self.metrics_calculator.reset()
