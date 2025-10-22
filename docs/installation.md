# Installation Guide

## Prerequisites

Before installing the Unified Memory Forensics Framework, ensure you have the following prerequisites:

### System Requirements
- **Operating System**: Windows 10/11, Ubuntu 18.04+, or macOS 10.15+
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: At least 2GB free space

### Required Tools
The framework integrates with the following memory forensics tools:

- **Volatility 3**: For Windows and Linux memory analysis
- **Rekall**: For cross-platform memory analysis
- **MemProcFS**: For live memory analysis

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/unified-memory-forensics.git
cd unified-memory-forensics

# Create virtual environment
python -m venv forensics-env

# Activate virtual environment
# Windows:
forensics-env\Scripts\activate
# Linux/macOS:
source forensics-env/bin/activate

# Install the framework
pip install -e .
```

### Method 2: Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/unified-memory-forensics.git
cd unified-memory-forensics

# Create virtual environment
python -m venv forensics-env

# Activate virtual environment
# Windows:
forensics-env\Scripts\activate
# Linux/macOS:
source forensics-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Tool Installation

### Volatility 3 Installation

#### Windows
```bash
# Using pip
pip install volatility3

# Or download from GitHub
git clone https://github.com/volatilityfoundation/volatility3.git
cd volatility3
python setup.py install
```

#### Linux/Ubuntu
```bash
# Using apt (if available)
sudo apt install volatility3

# Or using pip
pip install volatility3
```

#### macOS
```bash
# Using Homebrew
brew install volatility3

# Or using pip
pip install volatility3
```

### Rekall Installation

#### All Platforms
```bash
# Using pip
pip install rekall-core

# Or from source
git clone https://github.com/google/rekall.git
cd rekall
python setup.py install
```

### MemProcFS Installation

#### Windows
```bash
# Download from GitHub releases
# https://github.com/ufrisk/MemProcFS/releases
# Extract and add to PATH
```

#### Linux
```bash
# Download from GitHub releases
# https://github.com/ufrisk/MemProcFS/releases
# Extract and add to PATH
```

## Verification

After installation, verify that everything is working correctly:

```bash
# Check framework installation
python -c "import unified_forensics; print('Framework installed successfully')"

# Check CLI
unified-forensics --help

# Run tests
pytest tests/ -v
```

## Troubleshooting

### Common Issues

#### 1. Python Version Issues
```bash
# Check Python version
python --version

# If version is too old, install Python 3.8+
# Windows: Download from python.org
# Linux: sudo apt install python3.8
# macOS: brew install python@3.8
```

#### 2. Virtual Environment Issues
```bash
# If virtual environment activation fails
# Windows:
python -m venv forensics-env --clear
forensics-env\Scripts\activate

# Linux/macOS:
python3 -m venv forensics-env --clear
source forensics-env/bin/activate
```

#### 3. Tool Installation Issues
```bash
# If tools are not found, check PATH
echo $PATH  # Linux/macOS
echo %PATH%  # Windows

# Add tools to PATH or install globally
pip install --user volatility3 rekall-core
```

#### 4. Permission Issues
```bash
# Linux/macOS: Use sudo if needed
sudo pip install -r requirements.txt

# Or install for user only
pip install --user -r requirements.txt
```

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/yourusername/unified-memory-forensics/issues)
2. Review the [Documentation](https://github.com/yourusername/unified-memory-forensics/wiki)
3. Contact: manoj.santhoju@student.ncirl.ie

## Next Steps

After successful installation:

1. Read the [User Guide](user-guide.md)
2. Try the [Quick Start](quick-start.md)
3. Explore the [Examples](examples.md)
4. Review the [API Documentation](api.md)
