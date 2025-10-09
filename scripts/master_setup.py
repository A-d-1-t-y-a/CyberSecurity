#!/usr/bin/env python3
"""
Master Setup Script for Memory Forensics Framework
Runs all weekly setup scripts in sequence
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import logging

class MasterSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for master script"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.project_root / "master_setup.log"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def run_week_script(self, week_num: int) -> bool:
        """
        Run a specific week's setup script
        
        Args:
            week_num: Week number (1-7)
            
        Returns:
            Success status
        """
        week_script = self.scripts_dir / f"week{week_num}" / "setup.py"
        
        if not week_script.exists():
            self.logger.error(f"Week {week_num} script not found: {week_script}")
            return False
        
        self.logger.info(f"Running Week {week_num} setup...")
        print(f"🚀 Starting Week {week_num} Setup")
        print("=" * 50)
        
        try:
            # Change to project root directory
            result = subprocess.run([
                sys.executable, str(week_script)
            ], cwd=self.project_root, check=True, capture_output=True, text=True)
            
            self.logger.info(f"Week {week_num} completed successfully")
            print(f"✅ Week {week_num} completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Week {week_num} failed: {e}")
            print(f"❌ Week {week_num} failed: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            return False
    
    def run_all_weeks(self, start_week: int = 1, end_week: int = 7) -> bool:
        """
        Run all weekly setup scripts
        
        Args:
            start_week: Starting week number
            end_week: Ending week number
            
        Returns:
            Success status
        """
        self.logger.info(f"Starting master setup: Weeks {start_week}-{end_week}")
        print(f"🎯 Running Master Setup: Weeks {start_week}-{end_week}")
        print("=" * 60)
        
        success_count = 0
        total_weeks = end_week - start_week + 1
        
        for week in range(start_week, end_week + 1):
            print(f"\n📅 Week {week} of {end_week}")
            print("-" * 30)
            
            if self.run_week_script(week):
                success_count += 1
                print(f"✅ Week {week} completed successfully")
            else:
                print(f"❌ Week {week} failed")
                # Ask user if they want to continue
                response = input(f"Week {week} failed. Continue with remaining weeks? (y/n): ")
                if response.lower() != 'y':
                    break
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Master Setup Summary")
        print(f"✅ Successful weeks: {success_count}/{total_weeks}")
        print(f"❌ Failed weeks: {total_weeks - success_count}/{total_weeks}")
        
        if success_count == total_weeks:
            print("🎉 All weeks completed successfully!")
            return True
        else:
            print("⚠️  Some weeks failed. Check logs for details.")
            return False
    
    def run_specific_week(self, week_num: int) -> bool:
        """
        Run a specific week's setup
        
        Args:
            week_num: Week number to run
            
        Returns:
            Success status
        """
        if week_num < 1 or week_num > 7:
            print(f"❌ Invalid week number: {week_num}. Must be 1-7.")
            return False
        
        print(f"🎯 Running Week {week_num} Setup")
        print("=" * 40)
        
        return self.run_week_script(week_num)
    
    def show_status(self):
        """Show current project status"""
        print("📊 Project Status")
        print("=" * 30)
        
        # Check which weeks have been completed
        completed_weeks = []
        for week in range(1, 8):
            week_dir = self.project_root / f"week{week}"
            if week_dir.exists() and (week_dir / "status.md").exists():
                completed_weeks.append(week)
        
        print(f"✅ Completed weeks: {completed_weeks}")
        print(f"⏳ Remaining weeks: {[w for w in range(1, 8) if w not in completed_weeks]}")
        
        # Check framework status
        try:
            sys.path.insert(0, str(self.project_root / "src"))
            from framework.unified_api import MemoryForensicsFramework
            
            framework = MemoryForensicsFramework()
            info = framework.get_framework_info()
            
            print(f"\n🔧 Framework Status:")
            print(f"   Name: {info['name']}")
            print(f"   Version: {info['version']}")
            print(f"   Platform: {info['platform']}")
            print(f"   Available tools: {[k for k, v in info['available_tools'].items() if v]}")
            
        except Exception as e:
            print(f"❌ Framework not properly initialized: {e}")
    
    def cleanup(self):
        """Cleanup temporary files and logs"""
        print("🧹 Cleaning up...")
        
        # Clean up logs
        log_files = [
            "master_setup.log",
            "week1_setup.log",
            "week2_setup.log",
            "week3_setup.log",
            "week4_setup.log",
            "week5_setup.log",
            "week6_setup.log",
            "week7_setup.log"
        ]
        
        for log_file in log_files:
            log_path = self.project_root / log_file
            if log_path.exists():
                try:
                    log_path.unlink()
                    print(f"✅ Removed: {log_file}")
                except Exception as e:
                    print(f"⚠️  Could not remove {log_file}: {e}")
        
        print("✅ Cleanup completed")

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Master Setup for Memory Forensics Framework")
    parser.add_argument("--week", type=int, help="Run specific week (1-7)")
    parser.add_argument("--start", type=int, default=1, help="Start week (default: 1)")
    parser.add_argument("--end", type=int, default=7, help="End week (default: 7)")
    parser.add_argument("--status", action="store_true", help="Show project status")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup temporary files")
    
    args = parser.parse_args()
    
    setup = MasterSetup()
    
    if args.status:
        setup.show_status()
        return
    
    if args.cleanup:
        setup.cleanup()
        return
    
    if args.week:
        success = setup.run_specific_week(args.week)
    else:
        success = setup.run_all_weeks(args.start, args.end)
    
    if success:
        print("\n🎉 Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
