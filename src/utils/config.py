"""
Configuration Management for Memory Forensics Framework
"""

import json
import yaml
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """
    Configuration manager for the memory forensics framework
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or "configs/framework_config.json"
        self.config = {}
        self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration"""
        self.config = {
            "framework": {
                "name": "Unified Memory Forensics Framework",
                "version": "1.0.0",
                "description": "Cross-platform memory forensics framework"
            },
            "tools": {
                "volatility": {
                    "enabled": True,
                    "command": "vol",
                    "timeout": 120,
                    "plugins": [
                        "pslist", "psscan", "pstree", "cmdline",
                        "filescan", "netscan", "connections", "sockets"
                    ]
                },
                "rekall": {
                    "enabled": True,
                    "command": "rekall",
                    "timeout": 120,
                    "plugins": [
                        "pslist", "psscan", "pstree", "cmdline",
                        "filescan", "netscan", "connections", "sockets"
                    ]
                },
                "memprocfs": {
                    "enabled": True,
                    "path": "C:/Tools/MemProcFS",
                    "timeout": 120,
                    "plugins": ["processes", "files", "registry", "network"]
                }
            },
            "semantic_analysis": {
                "enabled": True,
                "categories": ["processes", "network", "files", "registry", "memory"],
                "scoring_weights": {
                    "processes": 0.3,
                    "network": 0.25,
                    "files": 0.2,
                    "registry": 0.15,
                    "memory": 0.1
                }
            },
            "cloud": {
                "enabled": True,
                "providers": ["aws", "azure", "gcp"],
                "temp_dir": "temp/cloud_dumps"
            },
            "output": {
                "format": "json",
                "include_metadata": True,
                "include_performance": True,
                "semantic_analysis": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/framework.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                        self.config.update(yaml.safe_load(f))
                    else:
                        self.config.update(json.load(f))
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
        
        return self.config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """
        Save configuration to file
        
        Args:
            config: Configuration to save (uses current config if None)
        """
        if config:
            self.config = config
        
        # Ensure directory exists
        Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_path, 'w') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False)
                else:
                    json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value by key
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific tool
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool configuration
        """
        return self.config.get("tools", {}).get(tool_name, {})
    
    def is_tool_enabled(self, tool_name: str) -> bool:
        """
        Check if a tool is enabled
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            True if tool is enabled
        """
        return self.get_tool_config(tool_name).get("enabled", False)
    
    def get_semantic_config(self) -> Dict[str, Any]:
        """
        Get semantic analysis configuration
        
        Returns:
            Semantic analysis configuration
        """
        return self.config.get("semantic_analysis", {})
    
    def get_cloud_config(self) -> Dict[str, Any]:
        """
        Get cloud configuration
        
        Returns:
            Cloud configuration
        """
        return self.config.get("cloud", {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """
        Get output configuration
        
        Returns:
            Output configuration
        """
        return self.config.get("output", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration
        
        Returns:
            Logging configuration
        """
        return self.config.get("logging", {})
