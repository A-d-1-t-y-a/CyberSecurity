#!/usr/bin/env python3
"""
Week 1 Setup Script - Cross-Platform Unified Memory Forensics Framework
Student: Manoj Santhoju (ID: 23394544)
Institution: National College of Ireland
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week1/logs/setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week1Setup:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.log_file = self.script_dir / 'logs' / 'validation.log'
        
    def setup_directories(self):
        """Create necessary directories for Week 1"""
        logger.info("Setting up directories...")
        
        directories = [
            'week1/logs',
            'week1/data', 
            'week1/reports',
            'week1/presentations',
            'src/framework',
            'src/utils',
            'src/tests'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
            
    def install_dependencies(self):
        """Install Python dependencies"""
        logger.info("Installing Python dependencies...")
        
        try:
            # Check if pip is available
            subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                         check=True, capture_output=True)
            
            # Install requirements
            requirements_file = self.project_root / 'requirements.txt'
            if requirements_file.exists():
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', '-r', 
                    str(requirements_file), '--user'
                ], check=True)
                logger.info("Dependencies installed from requirements.txt")
            else:
                # Install basic dependencies
                basic_deps = [
                    'volatility3', 'rekall', 'memprocfs', 'pandas', 
                    'numpy', 'scipy', 'jsonschema', 'pytest'
                ]
                for dep in basic_deps:
                    try:
                        subprocess.run([
                            sys.executable, '-m', 'pip', 'install', 
                            dep, '--user'
                        ], check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        logger.warning(f"Failed to install {dep}")
                        
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
            
        return True
        
    def install_forensics_tools(self):
        """Install memory forensics tools"""
        logger.info("Installing memory forensics tools...")
        
        tools = {
            'volatility3': 'vol',
            'rekall': 'rekall', 
            'memprocfs': 'memprocfs'
        }
        
        for tool, command in tools.items():
            try:
                # Check if tool is already installed
                result = subprocess.run([command, '--help'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"{tool} already installed")
                    continue
                    
            except FileNotFoundError:
                pass
                
            # Install tool
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', 
                    tool, '--user'
                ], check=True, capture_output=True)
                logger.info(f"{tool} installed successfully")
                
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to install {tool}: {e}")
                
    def download_sample_data(self):
        """Download sample memory dumps"""
        logger.info("Downloading sample memory dumps...")
        
        data_dir = self.script_dir / 'data'
        data_dir.mkdir(exist_ok=True)
        
        # Create sample files (synthetic data only)
        sample_files = {
            'sample_windows.dmp': 'Sample Windows memory dump placeholder',
            'sample_linux.dmp': 'Sample Linux memory dump placeholder', 
            'sample_macos.dmp': 'Sample macOS memory dump placeholder'
        }
        
        for filename, content in sample_files.items():
            file_path = data_dir / filename
            if not file_path.exists():
                file_path.write_text(content)
                logger.info(f"Created {filename}")
                
    def run(self):
        """Run Week 1 setup"""
        logger.info("Starting Week 1 setup...")
        
        try:
            self.setup_directories()
            self.install_dependencies()
            self.install_forensics_tools()
            self.download_sample_data()
            
            logger.info("Week 1 setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Week 1 setup failed: {e}")
            return False

if __name__ == "__main__":
    setup = Week1Setup()
    success = setup.run()
    sys.exit(0 if success else 1)
