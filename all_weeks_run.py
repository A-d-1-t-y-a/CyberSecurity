#!/usr/bin/env python3
"""
Master Script - Run All Weeks
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
        logging.FileHandler('all_weeks_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AllWeeksRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.weeks = [1, 2, 3, 4, 5, 6, 7]
        
    def run_week(self, week_num):
        """Run a specific week's complete_run script"""
        logger.info(f"Running Week {week_num}...")
        
        week_dir = self.project_root / f"week{week_num}"
        complete_run_py = week_dir / "complete_run.py"
        complete_run_bat = week_dir / "complete_run.bat"
        
        # Try Python script first
        if complete_run_py.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(complete_run_py)],
                    cwd=str(week_dir),
                    capture_output=True,
                    text=True,
                    timeout=1800  # 30 minute timeout per week
                )
                
                if result.returncode == 0:
                    logger.info(f"Week {week_num} completed successfully")
                    return True
                else:
                    logger.error(f"Week {week_num} failed: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                logger.error(f"Week {week_num} timed out")
                return False
            except Exception as e:
                logger.error(f"Week {week_num} failed with exception: {e}")
                return False
                
        # Try batch script on Windows
        elif complete_run_bat.exists() and os.name == 'nt':
            try:
                result = subprocess.run(
                    [str(complete_run_bat)],
                    cwd=str(week_dir),
                    capture_output=True,
                    text=True,
                    timeout=1800  # 30 minute timeout per week
                )
                
                if result.returncode == 0:
                    logger.info(f"Week {week_num} completed successfully")
                    return True
                else:
                    logger.error(f"Week {week_num} failed: {result.stderr}")
                    return False
                    
            except subprocess.TimeoutExpired:
                logger.error(f"Week {week_num} timed out")
                return False
            except Exception as e:
                logger.error(f"Week {week_num} failed with exception: {e}")
                return False
        else:
            logger.error(f"Week {week_num} complete_run script not found")
            return False
            
    def validate_week(self, week_num):
        """Validate that a week's deliverables are complete"""
        logger.info(f"Validating Week {week_num}...")
        
        week_dir = self.project_root / f"week{week_num}"
        
        # Check for required files
        required_files = [
            f"week{week_num}/complete_run.py",
            f"week{week_num}/complete_run.bat", 
            f"week{week_num}/explanations.txt",
            f"week{week_num}/report.md",
            f"week{week_num}/presentations/presentation.md"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                missing_files.append(file_path)
                
        if missing_files:
            logger.warning(f"Week {week_num} missing files: {missing_files}")
            return False
        else:
            logger.info(f"Week {week_num} validation passed")
            return True
            
    def check_line_counts(self):
        """Check that all Python files are under 300 lines"""
        logger.info("Checking line counts for all weeks...")
        
        for week_num in self.weeks:
            week_dir = self.project_root / f"week{week_num}"
            
            if week_dir.exists():
                python_files = list(week_dir.glob("*.py"))
                
                for py_file in python_files:
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            line_count = len(lines)
                            
                        if line_count > 300:
                            logger.warning(f"{py_file} has {line_count} lines (exceeds 300 limit)")
                        else:
                            logger.info(f"{py_file} has {line_count} lines (within limit)")
                            
                    except Exception as e:
                        logger.error(f"Error checking {py_file}: {e}")
                        
    def run_git_operations(self):
        """Run git operations to commit and push all changes"""
        logger.info("Running git operations...")
        
        try:
            # Change to project root
            os.chdir(self.project_root)
            
            # Add all files
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit changes
            commit_message = f"Complete project generation - All weeks ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
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
            
    def run(self, start_week=1, end_week=7):
        """Run all weeks from start_week to end_week"""
        logger.info(f"Starting all weeks run (Week {start_week} to {end_week})...")
        
        results = {}
        
        for week_num in range(start_week, end_week + 1):
            logger.info(f"Processing Week {week_num}...")
            
            # Run the week
            success = self.run_week(week_num)
            results[week_num] = success
            
            if not success:
                logger.error(f"Week {week_num} failed, but continuing...")
                
        # Validate all weeks
        logger.info("Validating all weeks...")
        validation_results = {}
        
        for week_num in range(start_week, end_week + 1):
            validation_success = self.validate_week(week_num)
            validation_results[week_num] = validation_success
            
        # Check line counts
        self.check_line_counts()
        
        # Git operations
        self.run_git_operations()
        
        # Summary
        logger.info("All weeks run completed")
        
        print("\n" + "="*80)
        print("ALL WEEKS RUN SUMMARY")
        print("="*80)
        
        for week_num in range(start_week, end_week + 1):
            status = "SUCCESS" if results.get(week_num, False) else "FAILED"
            validation = "PASSED" if validation_results.get(week_num, False) else "FAILED"
            print(f"Week {week_num}: Run={status}, Validation={validation}")
            
        print("="*80)
        
        # Overall success
        overall_success = all(results.get(week, False) for week in range(start_week, end_week + 1))
        
        if overall_success:
            print("All weeks completed successfully!")
        else:
            print("Some weeks failed. Check logs for details.")
            
        print("="*80)
        
        return overall_success

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run all weeks of the Memory Forensics Framework project')
    parser.add_argument('--start', type=int, default=1, help='Start week (default: 1)')
    parser.add_argument('--end', type=int, default=7, help='End week (default: 7)')
    parser.add_argument('--week', type=int, help='Run specific week only')
    
    args = parser.parse_args()
    
    runner = AllWeeksRunner()
    
    if args.week:
        success = runner.run(args.week, args.week)
    else:
        success = runner.run(args.start, args.end)
        
    sys.exit(0 if success else 1)
