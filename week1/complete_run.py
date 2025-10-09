#!/usr/bin/env python3
"""
Week 1 Master Runner - Complete Week 1 Execution
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
        logging.FileHandler('week1/logs/complete_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week1CompleteRun:
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
        """Validate that all Week 1 deliverables are generated"""
        logger.info("Validating Week 1 deliverables...")
        
        required_files = [
            'week1/setup.py',
            'week1/analysis.py', 
            'week1/reports.py',
            'week1/presentation.py',
            'week1/complete_run.py',
            'week1/explanations.txt',
            'week1/report.md',
            'week1/reports/literature_review.md',
            'week1/reports/tool_analysis.md',
            'week1/presentations/presentation.md',
            'week1/logs/setup.log',
            'week1/logs/analysis.log',
            'week1/logs/reports.log',
            'week1/logs/presentation.log',
            'week1/logs/complete_run.log'
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
            logger.info("All Week 1 deliverables validated successfully")
            return True
            
    def check_line_counts(self):
        """Check that all Python files are under 300 lines"""
        logger.info("Checking line counts...")
        
        python_files = [
            'week1/setup.py',
            'week1/analysis.py',
            'week1/reports.py', 
            'week1/presentation.py',
            'week1/complete_run.py'
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
            
            # Add all Week 1 files
            subprocess.run(['git', 'add', 'week1/'], check=True)
            
            # Commit changes
            commit_message = f"Week 1: Foundation & Literature Review - Complete deliverables generated ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
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
        """Run complete Week 1 workflow"""
        logger.info("Starting Week 1 complete run...")
        
        # Step 1: Setup
        if not self.run_script('setup', 'Week 1 Setup'):
            logger.error("Week 1 setup failed")
            return False
            
        # Step 2: Analysis
        if not self.run_script('analysis', 'Week 1 Analysis'):
            logger.error("Week 1 analysis failed")
            return False
            
        # Step 3: Reports
        if not self.run_script('reports', 'Week 1 Reports'):
            logger.error("Week 1 reports failed")
            return False
            
        # Step 4: Presentation
        if not self.run_script('presentation', 'Week 1 Presentation'):
            logger.error("Week 1 presentation failed")
            return False
            
        # Step 5: Validation
        if not self.validate_deliverables():
            logger.error("Week 1 deliverables validation failed")
            return False
            
        # Step 6: Line count check
        self.check_line_counts()
        
        # Step 7: Git operations
        self.run_git_operations()
        
        logger.info("Week 1 complete run finished successfully")
        return True

if __name__ == "__main__":
    runner = Week1CompleteRun()
    success = runner.run()
    
    if success:
        print("\n" + "="*60)
        print("Week 1 Complete Run - SUCCESS")
        print("="*60)
        print("All Week 1 deliverables have been generated successfully.")
        print("Check the week1/ directory for all outputs.")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("Week 1 Complete Run - FAILED")
        print("="*60)
        print("Some Week 1 deliverables failed to generate.")
        print("Check the logs in week1/logs/ for details.")
        print("="*60)
        
    sys.exit(0 if success else 1)
