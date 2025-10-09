"""
Logging Configuration for Memory Forensics Framework
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional

def setup_logger(name: str, 
                 level: str = "INFO",
                 log_file: Optional[str] = None,
                 max_size: str = "10MB",
                 backup_count: int = 5) -> logging.Logger:
    """
    Setup logger for the memory forensics framework
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Log file path
        max_size: Maximum log file size
        backup_count: Number of backup files
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Parse max_size (e.g., "10MB" -> 10 * 1024 * 1024)
        size_bytes = parse_size(max_size)
        
        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=size_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def parse_size(size_str: str) -> int:
    """
    Parse size string to bytes
    
    Args:
        size_str: Size string (e.g., "10MB", "1GB")
        
    Returns:
        Size in bytes
    """
    size_str = size_str.upper()
    
    if size_str.endswith('KB'):
        return int(size_str[:-2]) * 1024
    elif size_str.endswith('MB'):
        return int(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith('GB'):
        return int(size_str[:-2]) * 1024 * 1024 * 1024
    else:
        return int(size_str)

def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
