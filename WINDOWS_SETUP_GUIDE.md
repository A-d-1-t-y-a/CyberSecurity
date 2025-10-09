# Windows Setup Guide - Memory Forensics Framework

## 🚀 Quick Start (Recommended)

### Option 1: One-Click Setup
```bash
# Double-click this file in Windows Explorer
scripts/run_all_weeks.bat
```

### Option 2: PowerShell Setup
```powershell
# Run in PowerShell (as Administrator if needed)
.\scripts\Setup-Windows.ps1
```

### Option 3: Python Setup
```bash
# Run in Command Prompt or PowerShell
python scripts/quick_start_windows.py
```

## 📋 Prerequisites

### Required Software
- **Python 3.8+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **Visual Studio Code** (optional) - Download from [code.visualstudio.com](https://code.visualstudio.com)

### System Requirements
- **OS**: Windows 10/11 (64-bit recommended)
- **RAM**: 8GB+ (16GB recommended for large memory dumps)
- **Storage**: 10GB+ free space
- **CPU**: Multi-core processor recommended

## 🔧 Manual Setup (Step-by-Step)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/memory-forensics-framework.git
cd memory-forensics-framework
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Run Setup Scripts
```bash
# Run all weeks automatically
python scripts/master_setup.py

# Or run individual weeks
python scripts/week1/setup.py
python scripts/week2/setup.py
python scripts/week3/setup.py
```

## 🧪 Testing the Framework

### Run All Tests
```bash
# Activate virtual environment first
venv\Scripts\activate.bat

# Run all tests
python -m pytest src/tests/ -v
```

### Run Specific Tests
```bash
# Test framework core
python -m pytest src/tests/test_framework.py -v

# Test tool wrappers
python -m pytest src/tests/test_tools.py -v

# Test semantic analyzer
python -m pytest src/tests/test_semantic.py -v
```

## 📁 Project Structure After Setup

```
memory-forensics-framework/
├── venv/                           # Virtual environment
│   ├── Scripts/
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── activate.bat
│   └── Lib/
├── src/                           # Source code
│   ├── framework/
│   │   ├── unified_api.py
│   │   ├── tool_wrappers.py
│   │   ├── semantic_analyzer.py
│   │   └── cloud_handler.py
│   ├── utils/
│   └── tests/
├── week1/                         # Week 1 deliverables
│   ├── reports/
│   ├── code/
│   ├── data/
│   ├── presentations/
│   └── status.md
├── week2/                         # Week 2 deliverables
├── week3/                         # Week 3 deliverables
├── scripts/                       # Automation scripts
├── docs/                          # Documentation
├── activate_venv.bat             # Activation script
└── VENV_SETUP_SUMMARY.md         # Setup summary
```

## 🎯 Using the Framework

### Basic Usage
```python
# Activate virtual environment
venv\Scripts\activate.bat

# Start Python
python

# Import and use framework
from src.framework.unified_api import MemoryForensicsFramework

# Initialize framework
framework = MemoryForensicsFramework()

# Analyze memory dump
result = framework.analyze_memory_dump("memory.dmp", os_type="windows")

# Export results
framework.export_results(result, "analysis_results.json")
```

### Command Line Usage
```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Run framework from command line
python -m src.framework.unified_api --dump memory.dmp --os windows

# With semantic analysis
python -m src.framework.unified_api --dump memory.dmp --os windows --semantic

# List available tools
python -m src.framework.unified_api --list-tools
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Python Not Found
```
Error: 'python' is not recognized as an internal or external command
```
**Solution**: 
- Install Python from [python.org](https://python.org)
- Add Python to PATH during installation
- Restart Command Prompt/PowerShell

#### 2. Virtual Environment Issues
```
Error: Failed to create virtual environment
```
**Solution**:
- Ensure Python 3.8+ is installed
- Run Command Prompt as Administrator
- Check disk space (need 1GB+ free)

#### 3. Permission Denied
```
Error: Permission denied when creating venv
```
**Solution**:
- Run Command Prompt as Administrator
- Check antivirus software (may block file creation)
- Try different directory location

#### 4. Dependencies Installation Failed
```
Error: Failed to install requirements
```
**Solution**:
- Upgrade pip: `python -m pip install --upgrade pip`
- Check internet connection
- Try installing packages individually

#### 5. Tests Failing
```
Error: Some tests are failing
```
**Solution**:
- Ensure virtual environment is activated
- Check Python version compatibility
- Install missing dependencies

### Debug Mode
```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Run with debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
python scripts/week1/setup.py
```

## 📊 Performance Optimization

### For Large Memory Dumps
- **Use SSD storage** for better I/O performance
- **Increase system RAM** (16GB+ recommended)
- **Close unnecessary applications** during analysis
- **Use analysis type "process"** for faster analysis

### System Optimization
```bash
# Check system resources
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%'); print(f'RAM: {psutil.virtual_memory().percent}%')"

# Monitor during analysis
python -c "import psutil; import time; [print(f'CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%') for _ in range(10)]"
```

## 🚀 Advanced Usage

### Batch Processing
```python
# Process multiple memory dumps
dumps = ["dump1.dmp", "dump2.dmp", "dump3.dmp"]
batch_results = framework.run_batch_analysis(dumps)
```

### Cloud Integration
```python
# Analyze cloud-stored memory dump
cloud_result = framework.analyze_memory_dump(
    "s3://bucket/memory.dmp",
    cloud_source="aws"
)
```

### Custom Configuration
```python
# Load custom configuration
framework = MemoryForensicsFramework("configs/custom_config.json")
```

## 📚 Documentation

### Complete Documentation
- **User Guide**: `docs/guides/user_guide.md`
- **API Documentation**: `docs/guides/api_documentation.md`
- **Technical Specs**: `docs/guides/technical_specs.md`
- **Repository Guide**: `COMPLETE_REPOSITORY_GUIDE.md`

### Weekly Reports
- **Week 1**: Literature review and foundation
- **Week 2**: Tool analysis and framework design
- **Week 3**: Core implementation and testing
- **Week 4**: Advanced features and comprehensive testing
- **Week 5**: Plugin system and cloud integration
- **Week 6**: Performance optimization and validation
- **Week 7**: Documentation and finalization

## 🎉 Success Indicators

### Setup Success
- ✅ Virtual environment created successfully
- ✅ All dependencies installed
- ✅ All 3 weeks completed
- ✅ All tests passing
- ✅ Documentation generated

### Framework Ready
- ✅ Core API working
- ✅ Tool integration complete
- ✅ Semantic analysis functional
- ✅ Cross-platform support
- ✅ Cloud integration ready

## 📞 Support

### Getting Help
1. **Check Documentation**: Read complete documentation
2. **Run Tests**: Verify installation with test suite
3. **Check Logs**: Review setup and execution logs
4. **GitHub Issues**: Report issues on repository

### Contact Information
- **Student**: Manoj Santhoju
- **Student ID**: 23394544
- **Institution**: National College of Ireland
- **Supervisor**: Dr. Zakaria Sabir
- **Email**: manoj.santhoju@student.ncirl.ie

## 🏆 Expected Outcomes

### Academic Deliverables
- **Research Report**: 4000+ word comprehensive report
- **Framework Documentation**: Complete technical documentation
- **Test Results**: Performance and accuracy benchmarks
- **Comparison Analysis**: Framework vs. existing tools
- **Presentation**: Final project presentation

### Technical Deliverables
- **Working Framework**: Functional cross-platform framework
- **Tool Integration**: Volatility, Rekall, MemProcFS integration
- **Test Suite**: Comprehensive testing framework
- **Documentation**: Professional-grade documentation
- **Automation**: Complete automation scripts

### Professional Impact
- **Portfolio Project**: Demonstrates advanced cybersecurity skills
- **Research Contribution**: Academic publication potential
- **Industry Application**: Real-world forensic tool
- **Career Advancement**: Shows technical and research capabilities

## 🎯 Next Steps

1. **Complete Setup**: Ensure all 3 weeks are completed
2. **Run Tests**: Verify framework functionality
3. **Continue Development**: Run remaining weeks (4-7)
4. **Customize**: Adapt framework to your needs
5. **Document**: Create your own documentation
6. **Present**: Prepare final presentation

Your Memory Forensics Framework is now ready for advanced research and professional use! 🎉
