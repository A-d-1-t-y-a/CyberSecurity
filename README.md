# Unified Memory Forensics Framework

A cross-platform unified framework for memory forensics analysis across Windows, Linux, and macOS.

## 🚀 QUICK START (Windows)

### Single Command Installation
```cmd
# Download and extract the project, then run:
install.bat
```

### Single Command Testing
```cmd
# After installation, test the framework:
test_framework.bat
```

### Single Command Usage
```cmd
# Activate environment and run:
run.bat
```

## Features

- **Unified Interface**: Single command for all memory forensics tools
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Automatic OS Detection**: Automatically detects operating system and selects appropriate tool
- **Standardized Output**: Consistent JSON output regardless of underlying tool
- **Plugin System**: Extensible architecture for custom analysis modules

## Installation (Manual)

### Prerequisites
- Python 3.8 or higher
- Windows 10/11, Ubuntu 18.04+, or macOS 10.15+

### Windows Setup
```cmd
# Create virtual environment
py -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install framework
pip install -e .
```

## Usage

### Basic Analysis
```cmd
py -m unified_forensics analyze memory_dump.mem
```

### Advanced Options
```cmd
py -m unified_forensics analyze memory_dump.mem --os windows --output results.json
```

### Plugin Usage
```cmd
py -m unified_forensics analyze memory_dump.mem --plugins malware,network
```

## Project Structure

```
unified-memory-forensics/
├── unified_forensics/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── framework.py
│   │   ├── os_detector.py
│   │   └── output_standardizer.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── volatility_wrapper.py
│   │   ├── rekall_wrapper.py
│   │   └── memprocfs_wrapper.py
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── malware_detector.py
│   │   └── network_analyzer.py
│   └── cli.py
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=unified_forensics

# Run specific test
pytest tests/test_framework.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
