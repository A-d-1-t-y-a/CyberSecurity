"""
Tool Wrappers for Memory Forensics Framework
Provides unified interface for Volatility, Rekall, and MemProcFS
"""

import os
import json
import subprocess
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import tempfile
import shutil

class ToolWrapper:
    """
    Unified wrapper for memory forensics tools
    Provides consistent interface for Volatility, Rekall, and MemProcFS
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = tempfile.mkdtemp(prefix="memforensics_")
        
        # Tool configurations
        self.tool_configs = {
            "volatility": {
                "command": "vol",
                "plugins": [
                    "pslist", "psscan", "pstree", "cmdline",
                    "filescan", "netscan", "connections", "sockets",
                    "handles", "mutantscan", "driverscan", "modules",
                    "svcscan", "shimcache", "prefetch", "mftparser"
                ],
                "output_format": "json"
            },
            "rekall": {
                "command": "rekall",
                "plugins": [
                    "pslist", "psscan", "pstree", "cmdline",
                    "filescan", "netscan", "connections", "sockets",
                    "handles", "mutantscan", "driverscan", "modules",
                    "svcscan", "shimcache", "prefetch", "mftparser"
                ],
                "output_format": "json"
            },
            "memprocfs": {
                "command": "MemProcFS",
                "plugins": ["processes", "files", "registry", "network"],
                "output_format": "json"
            }
        }
    
    def analyze_dump(self, 
                    memory_dump_path: str, 
                    tool_name: str, 
                    analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze memory dump using specified tool
        
        Args:
            memory_dump_path: Path to memory dump
            tool_name: Name of the tool to use
            analysis_type: Type of analysis to perform
            
        Returns:
            Analysis results
        """
        self.logger.info(f"Analyzing dump with {tool_name}: {memory_dump_path}")
        
        if tool_name == "volatility":
            return self._analyze_with_volatility(memory_dump_path, analysis_type)
        elif tool_name == "rekall":
            return self._analyze_with_rekall(memory_dump_path, analysis_type)
        elif tool_name == "memprocfs":
            return self._analyze_with_memprocfs(memory_dump_path, analysis_type)
        else:
            raise ValueError(f"Unsupported tool: {tool_name}")
    
    def _analyze_with_volatility(self, 
                                memory_dump_path: str, 
                                analysis_type: str) -> Dict[str, Any]:
        """Analyze memory dump using Volatility"""
        results = {
            "tool": "volatility",
            "analysis_type": analysis_type,
            "plugins": {},
            "metadata": {}
        }
        
        # Get image info first
        try:
            info_result = subprocess.run([
                "vol", "-f", memory_dump_path, "imageinfo"
            ], capture_output=True, text=True, timeout=60)
            
            if info_result.returncode == 0:
                results["metadata"]["imageinfo"] = info_result.stdout
                
                # Extract profile if available
                profile = self._extract_volatility_profile(info_result.stdout)
                if profile:
                    results["metadata"]["profile"] = profile
        except subprocess.TimeoutExpired:
            self.logger.warning("Volatility imageinfo timed out")
        except Exception as e:
            self.logger.error(f"Volatility imageinfo failed: {e}")
        
        # Run plugins based on analysis type
        plugins_to_run = self._get_plugins_for_analysis("volatility", analysis_type)
        
        for plugin in plugins_to_run:
            try:
                plugin_result = self._run_volatility_plugin(
                    memory_dump_path, plugin, results.get("metadata", {}).get("profile")
                )
                if plugin_result:
                    results["plugins"][plugin] = plugin_result
            except Exception as e:
                self.logger.error(f"Plugin {plugin} failed: {e}")
                results["plugins"][plugin] = {"error": str(e)}
        
        return results
    
    def _analyze_with_rekall(self, 
                           memory_dump_path: str, 
                           analysis_type: str) -> Dict[str, Any]:
        """Analyze memory dump using Rekall"""
        results = {
            "tool": "rekall",
            "analysis_type": analysis_type,
            "plugins": {},
            "metadata": {}
        }
        
        # Get image info first
        try:
            info_result = subprocess.run([
                "rekall", "-f", memory_dump_path, "imageinfo"
            ], capture_output=True, text=True, timeout=60)
            
            if info_result.returncode == 0:
                results["metadata"]["imageinfo"] = info_result.stdout
        except subprocess.TimeoutExpired:
            self.logger.warning("Rekall imageinfo timed out")
        except Exception as e:
            self.logger.error(f"Rekall imageinfo failed: {e}")
        
        # Run plugins based on analysis type
        plugins_to_run = self._get_plugins_for_analysis("rekall", analysis_type)
        
        for plugin in plugins_to_run:
            try:
                plugin_result = self._run_rekall_plugin(memory_dump_path, plugin)
                if plugin_result:
                    results["plugins"][plugin] = plugin_result
            except Exception as e:
                self.logger.error(f"Plugin {plugin} failed: {e}")
                results["plugins"][plugin] = {"error": str(e)}
        
        return results
    
    def _analyze_with_memprocfs(self, 
                              memory_dump_path: str, 
                              analysis_type: str) -> Dict[str, Any]:
        """Analyze memory dump using MemProcFS (Windows only)"""
        results = {
            "tool": "memprocfs",
            "analysis_type": analysis_type,
            "plugins": {},
            "metadata": {}
        }
        
        # MemProcFS is a file system, so we mount it and analyze
        try:
            mount_point = os.path.join(self.temp_dir, "memprocfs")
            os.makedirs(mount_point, exist_ok=True)
            
            # Mount MemProcFS (this is a simplified version)
            # In reality, you would use the MemProcFS API
            results["metadata"]["mount_point"] = mount_point
            results["metadata"]["status"] = "mounted"
            
            # Analyze mounted file system
            plugins_to_run = self._get_plugins_for_analysis("memprocfs", analysis_type)
            
            for plugin in plugins_to_run:
                try:
                    plugin_result = self._run_memprocfs_plugin(mount_point, plugin)
                    if plugin_result:
                        results["plugins"][plugin] = plugin_result
                except Exception as e:
                    self.logger.error(f"Plugin {plugin} failed: {e}")
                    results["plugins"][plugin] = {"error": str(e)}
        
        except Exception as e:
            self.logger.error(f"MemProcFS analysis failed: {e}")
            results["error"] = str(e)
        
        return results
    
    def _get_plugins_for_analysis(self, tool_name: str, analysis_type: str) -> List[str]:
        """Get plugins to run based on analysis type"""
        base_plugins = ["pslist", "psscan", "cmdline"]
        
        if analysis_type == "comprehensive":
            return self.tool_configs[tool_name]["plugins"]
        elif analysis_type == "process":
            return ["pslist", "psscan", "pstree", "cmdline"]
        elif analysis_type == "network":
            return ["netscan", "connections", "sockets"]
        elif analysis_type == "files":
            return ["filescan", "handles", "prefetch"]
        elif analysis_type == "malware":
            return ["pslist", "psscan", "handles", "mutantscan", "driverscan"]
        else:
            return base_plugins
    
    def _run_volatility_plugin(self, 
                              memory_dump_path: str, 
                              plugin: str, 
                              profile: Optional[str] = None) -> Dict[str, Any]:
        """Run a Volatility plugin"""
        cmd = ["vol", "-f", memory_dump_path]
        
        if profile:
            cmd.extend(["--profile", profile])
        
        cmd.append(plugin)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": result.stdout,
                    "plugin": plugin
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "plugin": plugin
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "Plugin execution timed out",
                "plugin": plugin
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "plugin": plugin
            }
    
    def _run_rekall_plugin(self, 
                          memory_dump_path: str, 
                          plugin: str) -> Dict[str, Any]:
        """Run a Rekall plugin"""
        cmd = ["rekall", "-f", memory_dump_path, plugin]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": result.stdout,
                    "plugin": plugin
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "plugin": plugin
                }
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "error": "Plugin execution timed out",
                "plugin": plugin
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "plugin": plugin
            }
    
    def _run_memprocfs_plugin(self, 
                            mount_point: str, 
                            plugin: str) -> Dict[str, Any]:
        """Run a MemProcFS plugin (simplified)"""
        # This is a simplified implementation
        # In reality, you would use the MemProcFS API
        
        plugin_path = os.path.join(mount_point, plugin)
        
        if os.path.exists(plugin_path):
            try:
                with open(plugin_path, 'r') as f:
                    content = f.read()
                
                return {
                    "status": "success",
                    "output": content,
                    "plugin": plugin
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "plugin": plugin
                }
        else:
            return {
                "status": "not_found",
                "error": f"Plugin path not found: {plugin_path}",
                "plugin": plugin
            }
    
    def _extract_volatility_profile(self, imageinfo_output: str) -> Optional[str]:
        """Extract Volatility profile from imageinfo output"""
        lines = imageinfo_output.split('\n')
        for line in lines:
            if 'Suggested Profile(s)' in line:
                # Extract profile from line like "Suggested Profile(s) : Win7SP1x64"
                parts = line.split(':')
                if len(parts) > 1:
                    profile = parts[1].strip().split()[0]
                    return profile
        return None
    
    def get_plugins(self, tool_name: str) -> List[str]:
        """Get available plugins for a tool"""
        return self.tool_configs.get(tool_name, {}).get("plugins", [])
    
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
        if tool_name == "volatility":
            return self._run_volatility_plugin(memory_dump_path, plugin_name)
        elif tool_name == "rekall":
            return self._run_rekall_plugin(memory_dump_path, plugin_name)
        elif tool_name == "memprocfs":
            return self._run_memprocfs_plugin(memory_dump_path, plugin_name)
        else:
            raise ValueError(f"Unsupported tool: {tool_name}")
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp directory: {e}")
    
    def __del__(self):
        """Destructor to cleanup temporary files"""
        self.cleanup()
