#!/usr/bin/env python3
"""
Week 5 Master Runner - Complete Week 5 Execution
Cross-Platform Unified Memory Forensics Framework
Student: Manoj Santhoju (ID: 23394544)
Institution: National College of Ireland
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week5/logs/complete_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week5CompleteRun:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.log_file = self.script_dir / 'logs' / 'validation.log'
        
    def run_script(self, script_name, description):
        """Run a Python script and log results"""
        logger.info(f"Running {description}...")
        
        script_path = self.script_dir / f"{script_name}.py"
        
        if not script_path.exists():
            logger.error(f"Script not found: {script_path}")
            return False
            
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                logger.info(f"{description} completed successfully")
                return True
            else:
                logger.error(f"{description} failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"{description} timed out")
            return False
        except Exception as e:
            logger.error(f"{description} failed with exception: {e}")
            return False
            
    def validate_deliverables(self):
        """Validate that all Week 5 deliverables are generated"""
        logger.info("Validating Week 5 deliverables...")
        
        required_files = [
            'week5/setup.py',
            'week5/cloud_integration.py', 
            'week5/reports.py',
            'week5/presentation.py',
            'week5/complete_run.py',
            'week5/explanations.txt',
            'week5/report.md',
            'week5/reports/plugin_system_report.md',
            'week5/presentations/presentation.md',
            'src/plugins/plugin_manager.py',
            'src/plugins/base_plugin.py',
            'src/auto_selection/auto_tool_selector.py',
            'src/cloud/cloud_handler.py',
            'week5/logs/setup.log',
            'week5/logs/cloud_integration.log',
            'week5/logs/reports.log',
            'week5/logs/presentation.log',
            'week5/logs/complete_run.log'
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            logger.warning(f"Missing files: {missing_files}")
            return False
        else:
            logger.info("All Week 5 deliverables validated successfully")
            return True
            
    def check_line_counts(self):
        """Check that all Python files are under 300 lines"""
        logger.info("Checking line counts...")
        
        python_files = [
            'week5/setup.py',
            'week5/cloud_integration.py',
            'week5/reports.py', 
            'week5/presentation.py',
            'week5/complete_run.py',
            'src/plugins/plugin_manager.py',
            'src/plugins/base_plugin.py',
            'src/auto_selection/auto_tool_selector.py',
            'src/cloud/cloud_handler.py'
        ]
        
        for file_path in python_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                with open(full_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    line_count = len(lines)
                    
                if line_count > 300:
                    logger.warning(f"{file_path} has {line_count} lines (exceeds 300 limit)")
                else:
                    logger.info(f"{file_path} has {line_count} lines (within limit)")
                    
    def run_git_operations(self):
        """Run git operations to commit and push changes"""
        logger.info("Running git operations...")
        
        try:
            # Change to project root
            os.chdir(self.project_root)
            
            # Add all Week 5 files
            subprocess.run(['git', 'add', 'week5/', 'src/plugins/', 'src/auto_selection/', 'src/cloud/'], check=True)
            
            # Commit changes
            commit_message = f"Week 5: Plugin System & Cloud Integration - Complete deliverables generated ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # Push to remote
            subprocess.run(['git', 'push', 'origin', 'main'], check=True)
            
            logger.info("Git operations completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.warning(f"Git operations failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Git operations failed with exception: {e}")
            return False
            
    def run(self):
        """Run complete Week 5 workflow"""
        logger.info("Starting Week 5 complete run...")
        
        # Step 1: Setup
        if not self.run_script('setup', 'Week 5 Setup'):
            logger.error("Week 5 setup failed")
            return False
            
        # Step 2: Cloud Integration
        if not self.run_script('cloud_integration', 'Week 5 Cloud Integration'):
            logger.error("Week 5 cloud integration failed")
            return False
            
        # Step 3: Reports
        if not self.run_script('reports', 'Week 5 Reports'):
            logger.error("Week 5 reports failed")
            return False
            
        # Step 4: Presentation
        if not self.run_script('presentation', 'Week 5 Presentation'):
            logger.error("Week 5 presentation failed")
            return False
            
        # Step 5: Validation
        if not self.validate_deliverables():
            logger.error("Week 5 deliverables validation failed")
            return False
            
        # Step 6: Line count check
        self.check_line_counts()
        
        # Step 7: Git operations
        self.run_git_operations()
        
        logger.info("Week 5 complete run finished successfully")
        return True

if __name__ == "__main__":
    runner = Week5CompleteRun()
    success = runner.run()
    
    if success:
        print("\n" + "="*60)
        print("Week 5 Complete Run - SUCCESS")
        print("="*60)
        print("All Week 5 deliverables have been generated successfully.")
        print("Check the week5/ and src/ directories for all outputs.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Week 5 Complete Run - FAILED")
        print("="*60)
        print("Some Week 5 deliverables failed to generate.")
        print("Check the logs in week5/logs/ for details.")
        print("="*60)
        
    sys.exit(0 if success else 1)
