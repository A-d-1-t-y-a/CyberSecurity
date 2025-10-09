# Cross-Platform Unified Memory Forensics Framework

## Project Overview

This repository contains the implementation of a **Cross-Platform Unified Memory Forensics Framework** as part of an MSc Cybersecurity practicum project. The framework extends the semantic approach from file system forensics to memory forensics, providing a unified interface for analyzing memory dumps across Windows, Linux, and macOS platforms.

## Research Foundation

### Base Paper Extension
This project extends the research from:
- **Base Paper**: "Cross-Platform File System Activity Monitoring and Forensics – A Semantic Approach"
- **Extension**: Adapting semantic methodology to memory forensics with unified API and cross-platform support
- **Additional Research**: "Semantic-Enhanced Memory Forensics for Cloud and Virtualized Systems" (2025)

### Key Contributions
1. **Unified API**: Single interface for multiple memory forensics tools
2. **Semantic Analysis**: Advanced pattern recognition adapted from file system forensics
3. **Cross-Platform Support**: Works seamlessly across Windows, Linux, and macOS
4. **Tool Integration**: Wrappers for Volatility, Rekall, and MemProcFS
5. **Cloud Support**: Basic handling of cloud memory dumps
6. **Automated Selection**: Intelligent OS and tool detection

## Installation

### Prerequisites
- Python 3.9+
- Git
- Virtualization software (VMware/VirtualBox)
- 16GB+ RAM (recommended)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/memory-forensics-framework.git
cd memory-forensics-framework

# Run setup script for your platform
# Windows
.\scripts\setup.ps1

# Linux/macOS
./scripts/setup.sh

# Universal Python setup
python scripts/setup.py
```

### Manual Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install memory forensics tools
pip install volatility3
pip install rekall
pip install psutil
pip install yara-python

# Install development tools
pip install pytest
pip install black
pip install flake8
```

## Project Structure

```
memory-forensics-framework/
├── README.md
├── requirements.txt
├── docs/
│   ├── reports/
│   ├── guides/
│   └── presentations/
├── scripts/
│   ├── setup.ps1          # Windows setup
│   ├── setup.sh           # Linux/macOS setup
│   ├── setup.py           # Universal setup
│   └── weekX/             # Weekly automation scripts
├── src/
│   ├── framework/
│   │   ├── unified_api.py
│   │   ├── tool_wrappers.py
│   │   ├── semantic_analyzer.py
│   │   └── cloud_handler.py
│   ├── utils/
│   └── tests/
├── week1/                  # Week 1 deliverables
├── week2/                  # Week 2 deliverables
├── week3/                  # Week 3 deliverables
├── week4/                  # Week 4 deliverables
├── week5/                  # Week 5 deliverables
├── week6/                  # Week 6 deliverables
└── week7/                  # Week 7 deliverables
```

## Usage

### Basic Framework Usage
```python
from src.framework.unified_api import MemoryForensicsFramework

# Initialize framework
framework = MemoryForensicsFramework()

# Analyze memory dump
result = framework.analyze_memory_dump("memory.dmp", os_type="windows")
print(f"Analysis completed using {result['tool_used']}")
print(f"Results: {result['analysis_results']}")
```

### Command Line Interface
```bash
# Analyze memory dump
python -m src.framework.unified_api --dump memory.dmp --os windows

# List available tools
python -m src.framework.unified_api --list-tools

# Run semantic analysis
python -m src.framework.unified_api --semantic --dump memory.dmp
```

## Weekly Progress

### Week 1-2: Foundation & Analysis
- Literature review and base paper analysis
- Tool capability assessment
- Framework architecture design
- Initial API specification

### Week 3-4: Core Implementation
- Tool wrapper development
- OS detection and tool selection
- Basic semantic analysis
- Cross-platform testing

### Week 5-6: Advanced Features
- Plugin system development
- Cloud dump handling
- Performance optimization
- Comprehensive validation

### Week 7: Documentation & Finalization
- Complete documentation
- Final testing and optimization
- Report generation
- Presentation preparation

## Testing

### Run All Tests
```bash
pytest src/tests/ -v
```

### Run Specific Test Suites
```bash
# Test framework core
pytest src/tests/test_framework.py -v

# Test tool wrappers
pytest src/tests/test_tools.py -v

# Test semantic analysis
pytest src/tests/test_semantic.py -v
```

### Cross-Platform Testing
```bash
# Test on Windows
python scripts/week4/test_windows.py

# Test on Linux
python scripts/week4/test_linux.py

# Test on macOS
python scripts/week4/test_macos.py
```

## Documentation

- **API Documentation**: `docs/guides/api_documentation.md`
- **User Guide**: `docs/guides/user_guide.md`
- **Technical Specifications**: `docs/guides/technical_specs.md`
- **Weekly Reports**: `docs/reports/weekX_report.md`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Academic References

### Base Papers
1. Cross-Platform File System Activity Monitoring and Forensics – A Semantic Approach
2. Semantic-Enhanced Memory Forensics for Cloud and Virtualized Systems (2025)

### Additional References
- Volatility Foundation. (2023). Volatility 3 Framework
- Rekall Project. (2023). Rekall Memory Forensics Framework
- MemProcFS. (2023). Memory Process File System

## AI Acknowledgment

This project utilizes AI-assisted development tools for code generation, documentation, and testing. All AI-generated content has been reviewed, validated, and customized for the specific requirements of this memory forensics framework.

## Contact

- **Student**: Manoj Santhoju
- **Student ID**: 23394544
- **Institution**: National College of Ireland
- **Supervisor**: Dr. Zakaria Sabir
- **Email**: manoj.santhoju@student.ncirl.ie
