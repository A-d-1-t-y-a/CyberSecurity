#!/bin/bash

echo "=========================================="
echo "UNIFIED MEMORY FORENSICS FRAMEWORK"
echo "Linux Setup Script"
echo "Author: Manoj Santhoju"
echo "Institution: National College of Ireland"
echo "=========================================="

# Check if Python 3 is installed
echo "[1] Checking Python 3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.11+ using:"
    echo "  sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

python3 --version
echo "SUCCESS: Python 3 is installed"

# Check if pip is installed
echo ""
echo "[2] Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3 using:"
    echo "  sudo apt install python3-pip"
    exit 1
fi

pip3 --version
echo "SUCCESS: pip3 is installed"

# Create virtual environment
echo ""
echo "[3] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "SUCCESS: Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "SUCCESS: Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "SUCCESS: Virtual environment activated"

# Upgrade pip
echo ""
echo "[5] Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip"
    exit 1
fi
echo "SUCCESS: pip upgraded"

# Install requirements
echo ""
echo "[6] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "SUCCESS: Dependencies installed"

# Install the framework
echo ""
echo "[7] Installing framework..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install framework"
    exit 1
fi
echo "SUCCESS: Framework installed"

# Create necessary directories
echo ""
echo "[8] Creating project directories..."
mkdir -p memory_dump_samples analysis_results performance_charts logs
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create directories"
    exit 1
fi
echo "SUCCESS: Directories created"

# Test framework installation
echo ""
echo "[9] Testing framework installation..."
python3 -m unified_forensics info
if [ $? -ne 0 ]; then
    echo "ERROR: Framework test failed"
    exit 1
fi
echo "SUCCESS: Framework test passed"

echo ""
echo "=========================================="
echo "SETUP COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo ""
echo "To activate the environment in future sessions:"
echo "  source venv/bin/activate"
echo ""
echo "To run the complete demo:"
echo "  python3 demo_framework.py"
echo ""
echo "To run quick tests:"
echo "  ./test_linux.sh"
echo ""
echo "To analyze a real memory dump:"
echo "  python3 -m unified_forensics analyze <dump.mem> --os-type linux --format summary --metrics"
echo ""
echo "To run experimental analysis:"
echo "  python3 -m unified_forensics experiment <dump.mem> --os-type linux --rates 1 --rates 10"
echo ""
