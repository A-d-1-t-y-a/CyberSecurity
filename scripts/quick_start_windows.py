#!/usr/bin/env python3
"""
Quick Start Script for Windows
One-click setup and run all 3 weeks
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Quick start for Windows users"""
    print("🚀 Memory Forensics Framework - Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path(__file__).parent.parent
    if not (project_root / "src").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("Expected structure: memory-forensics-framework/scripts/quick_start_windows.py")
        return False
    
    print(f"📁 Project root: {project_root}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {python_version.major}.{python_version.minor}")
        return False
    
    print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    # Run the Windows venv setup
    print("\n🔧 Running Windows Virtual Environment Setup...")
    try:
        result = subprocess.run([
            sys.executable, "scripts/windows_venv_setup.py"
        ], cwd=project_root, check=True)
        
        print("\n🎉 Setup completed successfully!")
        print("\n📋 What was created:")
        print("- Virtual environment: venv/")
        print("- Week 1 deliverables: week1/")
        print("- Week 2 deliverables: week2/")
        print("- Week 3 deliverables: week3/")
        print("- Activation script: activate_venv.bat")
        print("- Summary report: VENV_SETUP_SUMMARY.md")
        
        print("\n🚀 Next steps:")
        print("1. Activate virtual environment: activate_venv.bat")
        print("2. Run remaining weeks: python scripts/week4/setup.py")
        print("3. Test framework: python -m pytest src/tests/ -v")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Quick start completed successfully!")
    else:
        print("\n❌ Quick start failed. Check the error messages above.")
    
    input("\nPress Enter to exit...")
