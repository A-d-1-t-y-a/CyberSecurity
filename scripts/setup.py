#!/usr/bin/env python3
"""
Universal Setup Script for Memory Forensics Framework
Supports Windows, Linux, and macOS platforms
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

class FrameworkSetup:
    def __init__(self):
        self.platform = platform.system().lower()
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / "scripts"
        self.src_dir = self.project_root / "src"
        
    def run_command(self, command, shell=True):
        """Run a command and return the result"""
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def check_python_version(self):
        """Check if Python version is 3.9+"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            print("❌ Python 3.9+ is required")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def install_requirements(self):
        """Install Python requirements"""
        print("📦 Installing Python requirements...")
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        success, stdout, stderr = self.run_command(f"pip install -r {requirements_file}")
        if success:
            print("✅ Python requirements installed successfully")
            return True
        else:
            print(f"❌ Failed to install requirements: {stderr}")
            return False
    
    def install_memory_forensics_tools(self):
        """Install memory forensics tools"""
        print("🔧 Installing memory forensics tools...")
        
        tools = [
            "volatility3",
            "rekall",
            "psutil",
            "yara-python"
        ]
        
        for tool in tools:
            print(f"Installing {tool}...")
            success, stdout, stderr = self.run_command(f"pip install {tool}")
            if success:
                print(f"✅ {tool} installed successfully")
            else:
                print(f"❌ Failed to install {tool}: {stderr}")
                return False
        
        return True
    
    def setup_project_structure(self):
        """Create project directory structure"""
        print("📁 Setting up project structure...")
        
        directories = [
            "src/framework",
            "src/utils",
            "src/tests",
            "docs/reports",
            "docs/guides",
            "docs/presentations",
            "data/dumps",
            "data/results",
            "logs",
            "week1", "week2", "week3", "week4", "week5", "week6", "week7"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        
        return True
    
    def create_gitignore(self):
        """Create .gitignore file"""
        print("📝 Creating .gitignore...")
        
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Memory dumps and sensitive data
data/dumps/*.dmp
data/dumps/*.raw
data/dumps/*.vmem
data/results/*.json
*.log

# OS specific
.DS_Store
Thumbs.db

# Project specific
logs/
temp/
cache/
"""
        
        gitignore_path = self.project_root / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content.strip())
        
        print("✅ .gitignore created")
        return True
    
    def verify_installation(self):
        """Verify that all tools are installed correctly"""
        print("🔍 Verifying installation...")
        
        # Test Python imports
        test_imports = [
            "volatility3",
            "rekall",
            "psutil",
            "yara"
        ]
        
        for module in test_imports:
            try:
                __import__(module)
                print(f"✅ {module} import successful")
            except ImportError:
                print(f"❌ {module} import failed")
                return False
        
        return True
    
    def run_tests(self):
        """Run basic tests to verify setup"""
        print("🧪 Running basic tests...")
        
        # Test framework import
        try:
            sys.path.insert(0, str(self.src_dir))
            from framework.unified_api import MemoryForensicsFramework
            framework = MemoryForensicsFramework()
            print("✅ Framework import successful")
        except ImportError as e:
            print(f"❌ Framework import failed: {e}")
            return False
        
        return True
    
    def setup_git(self):
        """Initialize git repository if not already done"""
        print("🔧 Setting up Git repository...")
        
        # Check if git is already initialized
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            print("✅ Git repository already initialized")
            return True
        
        # Initialize git repository
        success, stdout, stderr = self.run_command("git init", cwd=self.project_root)
        if success:
            print("✅ Git repository initialized")
            
            # Add all files
            self.run_command("git add .", cwd=self.project_root)
            
            # Make initial commit
            self.run_command('git commit -m "Initial commit: Framework setup"', cwd=self.project_root)
            
            return True
        else:
            print(f"❌ Failed to initialize git: {stderr}")
            return False
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Memory Forensics Framework Setup")
        print("=" * 50)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Setup project structure
        if not self.setup_project_structure():
            return False
        
        # Create .gitignore
        if not self.create_gitignore():
            return False
        
        # Install requirements
        if not self.install_requirements():
            return False
        
        # Install memory forensics tools
        if not self.install_memory_forensics_tools():
            return False
        
        # Verify installation
        if not self.verify_installation():
            return False
        
        # Setup git
        if not self.setup_git():
            return False
        
        print("=" * 50)
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Run tests: pytest src/tests/ -v")
        print("2. Start with Week 1: python scripts/week1/setup.py")
        print("3. Read documentation: docs/guides/user_guide.md")
        
        return True

def main():
    """Main setup function"""
    setup = FrameworkSetup()
    success = setup.run_setup()
    
    if success:
        sys.exit(0)
    else:
        print("❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
