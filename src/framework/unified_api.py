"""
Unified Memory Forensics Framework API
Main entry point for cross-platform memory forensics analysis
"""

import os
import json
import logging
import platform
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import subprocess
import time

from .tool_wrappers import ToolWrapper
from .semantic_analyzer import SemanticAnalyzer
from .cloud_handler import CloudHandler
from ..utils.config import ConfigManager
from ..utils.logger import setup_logger

class MemoryForensicsFramework:
    """
    Unified Memory Forensics Framework
    
    Provides a single interface for memory forensics across different
    operating systems and tools, extending semantic analysis from
    file system forensics to memory forensics.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Memory Forensics Framework
        
        Args:
            config_path: Path to configuration file
        """
        self.name = "Unified Memory Forensics Framework"
        self.version = "1.0.0"
        self.platform = platform.system().lower()
        
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.logger = setup_logger(__name__)
        self.semantic_analyzer = SemanticAnalyzer()
        self.cloud_handler = CloudHandler()
        self.tool_wrapper = ToolWrapper()
        
        # Load configuration
        self.config = self.config_manager.load_config()
        
        # Initialize available tools
        self.available_tools = self._detect_available_tools()
        
        self.logger.info(f"Initialized {self.name} v{self.version} on {self.platform}")
    
    def _detect_available_tools(self) -> Dict[str, bool]:
        """
        Detect available memory forensics tools
        
        Returns:
            Dictionary of tool availability
        """
        tools = {
            "volatility": False,
            "rekall": False,
            "memprocfs": False
        }
        
        # Check Volatility
        try:
            result = subprocess.run(["vol", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            tools["volatility"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check Rekall
        try:
            result = subprocess.run(["rekall", "--help"], 
                                  capture_output=True, text=True, timeout=10)
            tools["rekall"] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Check MemProcFS (Windows only)
        if self.platform == "windows":
            memprocfs_path = self.config.get("tools", {}).get("memprocfs", {}).get("path")
            if memprocfs_path and os.path.exists(memprocfs_path):
                tools["memprocfs"] = True
        
        self.logger.info(f"Available tools: {[k for k, v in tools.items() if v]}")
        return tools
    
    def detect_os(self, memory_dump_path: str) -> str:
        """
        Detect operating system from memory dump
        
        Args:
            memory_dump_path: Path to memory dump file
            
        Returns:
            Detected operating system
        """
        self.logger.info(f"Detecting OS for memory dump: {memory_dump_path}")
        
        # Use Volatility for OS detection
        if self.available_tools.get("volatility"):
            try:
                result = subprocess.run([
                    "vol", "-f", memory_dump_path, "imageinfo"
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    output = result.stdout.lower()
                    if "windows" in output:
                        return "windows"
                    elif "linux" in output:
                        return "linux"
                    elif "mac" in output or "darwin" in output:
                        return "macos"
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                pass
        
        # Fallback to file extension or manual detection
        dump_path = Path(memory_dump_path)
        if dump_path.suffix.lower() in ['.dmp', '.raw', '.vmem']:
            # Try to detect from filename or use default
            filename = dump_path.name.lower()
            if "windows" in filename:
                return "windows"
            elif "linux" in filename:
                return "linux"
            elif "mac" in filename or "darwin" in filename:
                return "macos"
        
        # Default fallback
        return "windows"
    
    def select_tool(self, os_type: str, analysis_type: str = "process") -> str:
        """
        Select the best tool for the given OS and analysis type
        
        Args:
            os_type: Target operating system
            analysis_type: Type of analysis to perform
            
        Returns:
            Selected tool name
        """
        self.logger.info(f"Selecting tool for OS: {os_type}, Analysis: {analysis_type}")
        
        # Tool selection logic based on OS and capabilities
        tool_preferences = {
            "windows": ["volatility", "rekall", "memprocfs"],
            "linux": ["volatility", "rekall"],
            "macos": ["rekall", "volatility"]
        }
        
        preferred_tools = tool_preferences.get(os_type.lower(), ["volatility"])
        
        for tool in preferred_tools:
            if self.available_tools.get(tool, False):
                self.logger.info(f"Selected tool: {tool}")
                return tool
        
        # Fallback to first available tool
        for tool, available in self.available_tools.items():
            if available:
                self.logger.warning(f"Using fallback tool: {tool}")
                return tool
        
        raise RuntimeError("No memory forensics tools available")
    
    def analyze_memory_dump(self, 
                           memory_dump_path: str, 
                           os_type: Optional[str] = None,
                           analysis_type: str = "comprehensive",
                           use_semantic: bool = True,
                           cloud_source: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze memory dump using the unified framework
        
        Args:
            memory_dump_path: Path to memory dump file
            os_type: Operating system type (auto-detected if None)
            analysis_type: Type of analysis to perform
            use_semantic: Whether to use semantic analysis
            cloud_source: Cloud source if analyzing cloud dump
            
        Returns:
            Analysis results dictionary
        """
        start_time = time.time()
        self.logger.info(f"Starting analysis of: {memory_dump_path}")
        
        try:
            # Handle cloud dumps
            if cloud_source:
                memory_dump_path = self.cloud_handler.download_dump(
                    memory_dump_path, cloud_source
                )
            
            # Detect OS if not provided
            if not os_type:
                os_type = self.detect_os(memory_dump_path)
            
            # Select appropriate tool
            selected_tool = self.select_tool(os_type, analysis_type)
            
            # Perform analysis using selected tool
            analysis_results = self.tool_wrapper.analyze_dump(
                memory_dump_path, selected_tool, analysis_type
            )
            
            # Apply semantic analysis if requested
            if use_semantic:
                semantic_results = self.semantic_analyzer.analyze(
                    analysis_results, os_type
                )
                analysis_results["semantic_analysis"] = semantic_results
            
            # Calculate performance metrics
            execution_time = time.time() - start_time
            
            # Compile results
            results = {
                "status": "success",
                "memory_dump": memory_dump_path,
                "os_type": os_type,
                "tool_used": selected_tool,
                "analysis_type": analysis_type,
                "execution_time": execution_time,
                "analysis_results": analysis_results,
                "framework_version": self.version,
                "timestamp": time.time()
            }
            
            self.logger.info(f"Analysis completed in {execution_time:.2f} seconds")
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "memory_dump": memory_dump_path,
                "timestamp": time.time()
            }
    
    def get_available_plugins(self, tool_name: str) -> List[str]:
        """
        Get available plugins for a specific tool
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            List of available plugins
        """
        return self.tool_wrapper.get_plugins(tool_name)
    
    def run_plugin(self, 
                   memory_dump_path: str, 
                   tool_name: str, 
                   plugin_name: str,
                   **kwargs) -> Dict[str, Any]:
        """
        Run a specific plugin on a memory dump
        
        Args:
            memory_dump_path: Path to memory dump
            tool_name: Name of the tool
            plugin_name: Name of the plugin
            **kwargs: Additional plugin arguments
            
        Returns:
            Plugin execution results
        """
        return self.tool_wrapper.run_plugin(
            memory_dump_path, tool_name, plugin_name, **kwargs
        )
    
    def export_results(self, 
                      results: Dict[str, Any], 
                      output_path: str,
                      format: str = "json") -> bool:
        """
        Export analysis results to file
        
        Args:
            results: Analysis results
            output_path: Output file path
            format: Export format (json, csv, xml)
            
        Returns:
            Success status
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            if format.lower() == "json":
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
            elif format.lower() == "csv":
                # Convert results to CSV format
                import pandas as pd
                df = pd.json_normalize(results)
                df.to_csv(output_path, index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Results exported to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False
    
    def get_framework_info(self) -> Dict[str, Any]:
        """
        Get framework information and status
        
        Returns:
            Framework information dictionary
        """
        return {
            "name": self.name,
            "version": self.version,
            "platform": self.platform,
            "available_tools": self.available_tools,
            "config": self.config,
            "semantic_analyzer": self.semantic_analyzer.get_info(),
            "cloud_handler": self.cloud_handler.get_info()
        }


def main():
    """Command line interface for the framework"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Forensics Framework")
    parser.add_argument("--dump", required=True, help="Path to memory dump")
    parser.add_argument("--os", help="Operating system type")
    parser.add_argument("--analysis", default="comprehensive", help="Analysis type")
    parser.add_argument("--semantic", action="store_true", help="Use semantic analysis")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--format", default="json", help="Output format")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--info", action="store_true", help="Show framework info")
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = MemoryForensicsFramework()
    
    if args.list_tools:
        print("Available tools:")
        for tool, available in framework.available_tools.items():
            status = "✓" if available else "✗"
            print(f"  {status} {tool}")
        return
    
    if args.info:
        info = framework.get_framework_info()
        print(json.dumps(info, indent=2))
        return
    
    # Analyze memory dump
    results = framework.analyze_memory_dump(
        args.dump,
        os_type=args.os,
        analysis_type=args.analysis,
        use_semantic=args.semantic
    )
    
    # Output results
    if args.output:
        framework.export_results(results, args.output, args.format)
        print(f"Results exported to: {args.output}")
    else:
        print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
