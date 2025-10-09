#!/usr/bin/env python3
"""
Week 2 Master Runner - Complete Week 2 Execution
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
        logging.FileHandler('week2/logs/complete_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week2CompleteRun:
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
        """Validate that all Week 2 deliverables are generated"""
        logger.info("Validating Week 2 deliverables...")
        
        required_files = [
            'week2/setup.py',
            'week2/analysis.py', 
            'week2/reports.py',
            'week2/presentation.py',
            'week2/complete_run.py',
            'week2/explanations.txt',
            'week2/report.md',
            'week2/reports/architecture_design.md',
            'week2/reports/api_specification.md',
            'week2/presentations/presentation.md',
            'week2/logs/setup.log',
            'week2/logs/analysis.log',
            'week2/logs/reports.log',
            'week2/logs/presentation.log',
            'week2/logs/complete_run.log'
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
            logger.info("All Week 2 deliverables validated successfully")
            return True
            
    def check_line_counts(self):
        """Check that all Python files are under 300 lines"""
        logger.info("Checking line counts...")
        
        python_files = [
            'week2/setup.py',
            'week2/analysis.py',
            'week2/reports.py', 
            'week2/presentation.py',
            'week2/complete_run.py'
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
            
            # Add all Week 2 files
            subprocess.run(['git', 'add', 'week2/'], check=True)
            
            # Commit changes
            commit_message = f"Week 2: Tool Analysis & Framework Design - Complete deliverables generated ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
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
        """Run complete Week 2 workflow"""
        logger.info("Starting Week 2 complete run...")
        
        # Step 1: Setup
        if not self.run_script('setup', 'Week 2 Setup'):
            logger.error("Week 2 setup failed")
            return False
            
        # Step 2: Analysis
        if not self.run_script('analysis', 'Week 2 Analysis'):
            logger.error("Week 2 analysis failed")
            return False
            
        # Step 3: Reports
        if not self.run_script('reports', 'Week 2 Reports'):
            logger.error("Week 2 reports failed")
            return False
            
        # Step 4: Presentation
        if not self.run_script('presentation', 'Week 2 Presentation'):
            logger.error("Week 2 presentation failed")
            return False
            
        # Step 5: Validation
        if not self.validate_deliverables():
            logger.error("Week 2 deliverables validation failed")
            return False
            
        # Step 6: Line count check
        self.check_line_counts()
        
        # Step 7: Git operations
        self.run_git_operations()
        
        logger.info("Week 2 complete run finished successfully")
        return True

if __name__ == "__main__":
    runner = Week2CompleteRun()
    success = runner.run()
    
    if success:
        print("\n" + "="*60)
        print("Week 2 Complete Run - SUCCESS")
        print("="*60)
        print("All Week 2 deliverables have been generated successfully.")
        print("Check the week2/ directory for all outputs.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Week 2 Complete Run - FAILED")
        print("="*60)
        print("Some Week 2 deliverables failed to generate.")
        print("Check the logs in week2/logs/ for details.")
        print("="*60)
        
    sys.exit(0 if success else 1)
