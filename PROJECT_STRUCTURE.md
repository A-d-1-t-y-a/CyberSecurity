# Memory Forensics Framework - Complete Repository Structure

## Overview
This repository contains a complete implementation of a **Cross-Platform Unified Memory Forensics Framework** for MSc Cybersecurity research. The framework extends semantic analysis from file system forensics to memory forensics, providing a unified interface for Volatility, Rekall, and MemProcFS.

## Repository Structure

```
memory-forensics-framework/
├── README.md                           # Project overview and installation guide
├── requirements.txt                    # Python dependencies
├── PROJECT_STRUCTURE.md               # This file - complete structure overview
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
│
├── docs/                              # Documentation
│   ├── guides/
│   │   ├── user_guide.md              # Comprehensive user guide
│   │   ├── api_documentation.md       # API reference
│   │   └── technical_specs.md         # Technical specifications
│   ├── reports/                       # Weekly reports
│   └── presentations/                 # Weekly presentations
│
├── scripts/                           # Automation scripts
│   ├── setup.py                       # Universal setup script
│   ├── setup.ps1                      # Windows PowerShell setup
│   ├── setup.sh                       # Linux/macOS bash setup
│   ├── master_setup.py                # Master script for all weeks
│   └── weekX/                         # Weekly automation scripts
│       ├── week1/
│       │   └── setup.py               # Week 1: Foundation & Literature Review
│       ├── week2/
│       │   └── setup.py               # Week 2: Tool Analysis & Framework Design
│       ├── week3/
│       │   └── setup.py               # Week 3: Core Implementation
│       ├── week4/
│       │   └── setup.py               # Week 4: Advanced Features & Testing
│       ├── week5/
│       │   └── setup.py               # Week 5: Plugin System & Cloud Integration
│       ├── week6/
│       │   └── setup.py               # Week 6: Performance Optimization & Validation
│       └── week7/
│           └── setup.py               # Week 7: Documentation & Finalization
│
├── src/                               # Source code
│   ├── framework/                     # Core framework modules
│   │   ├── __init__.py
│   │   ├── unified_api.py             # Main unified API
│   │   ├── tool_wrappers.py           # Tool wrappers (Volatility, Rekall, MemProcFS)
│   │   ├── semantic_analyzer.py       # Semantic analysis engine
│   │   └── cloud_handler.py           # Cloud dump processing
│   ├── utils/                         # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuration management
│   │   └── logger.py                  # Logging configuration
│   └── tests/                         # Test suite
│       ├── __init__.py
│       ├── test_framework.py          # Framework tests
│       ├── test_tools.py              # Tool wrapper tests
│       ├── test_semantic.py           # Semantic analyzer tests
│       └── test_cloud.py              # Cloud handler tests
│
├── week1/                             # Week 1 deliverables
│   ├── reports/
│   │   └── literature_review.md       # Literature review document
│   ├── code/                          # Week 1 code
│   ├── data/                          # Week 1 data
│   ├── presentations/
│   │   └── week1_presentation.md      # Week 1 presentation
│   ├── scripts/                       # Week 1 scripts
│   └── status.md                      # Week 1 status report
│
├── week2/                             # Week 2 deliverables
│   ├── reports/
│   │   └── tool_analysis.md           # Tool analysis report
│   ├── code/                          # Week 2 code
│   ├── data/                          # Week 2 data
│   ├── presentations/
│   │   └── week2_presentation.md      # Week 2 presentation
│   ├── scripts/                       # Week 2 scripts
│   └── status.md                      # Week 2 status report
│
├── week3/                             # Week 3 deliverables
│   ├── reports/
│   │   └── implementation_report.md   # Implementation report
│   ├── code/                          # Week 3 code
│   ├── data/                          # Week 3 data
│   ├── presentations/
│   │   └── week3_presentation.md      # Week 3 presentation
│   ├── scripts/                       # Week 3 scripts
│   └── status.md                      # Week 3 status report
│
├── week4/                             # Week 4 deliverables
│   ├── reports/
│   │   └── advanced_features.md       # Advanced features report
│   ├── code/                          # Week 4 code
│   ├── data/                          # Week 4 data
│   ├── presentations/
│   │   └── week4_presentation.md      # Week 4 presentation
│   ├── scripts/                       # Week 4 scripts
│   └── status.md                      # Week 4 status report
│
├── week5/                             # Week 5 deliverables
│   ├── reports/
│   │   └── plugin_system.md           # Plugin system report
│   ├── code/                          # Week 5 code
│   ├── data/                          # Week 5 data
│   ├── presentations/
│   │   └── week5_presentation.md      # Week 5 presentation
│   ├── scripts/                       # Week 5 scripts
│   └── status.md                      # Week 5 status report
│
├── week6/                             # Week 6 deliverables
│   ├── reports/
│   │   └── performance_optimization.md # Performance optimization report
│   ├── code/                          # Week 6 code
│   ├── data/                          # Week 6 data
│   ├── presentations/
│   │   └── week6_presentation.md      # Week 6 presentation
│   ├── scripts/                       # Week 6 scripts
│   └── status.md                      # Week 6 status report
│
├── week7/                             # Week 7 deliverables
│   ├── reports/
│   │   └── final_report.md            # Final project report
│   ├── code/                          # Week 7 code
│   ├── data/                          # Week 7 data
│   ├── presentations/
│   │   └── week7_presentation.md      # Final presentation
│   ├── scripts/                       # Week 7 scripts
│   └── status.md                      # Week 7 status report
│
├── data/                              # Project data
│   ├── dumps/                         # Memory dump files (gitignored)
│   └── results/                       # Analysis results (gitignored)
│
├── logs/                              # Log files (gitignored)
│   └── framework.log                  # Framework logs
│
└── configs/                           # Configuration files
    └── framework_config.json          # Framework configuration
```

## Key Features

### 1. Unified API
- **Single Interface**: One API for all memory forensics tools
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Tool Integration**: Seamless integration with Volatility, Rekall, and MemProcFS
- **Automatic Selection**: Intelligent tool selection based on OS and analysis type

### 2. Semantic Analysis
- **Pattern Recognition**: Advanced pattern recognition for memory artifacts
- **Threat Detection**: Automated threat indicator identification
- **Semantic Scoring**: Quantitative analysis of memory patterns
- **Recommendations**: Automated recommendations based on analysis

### 3. Cloud Integration
- **Multi-Cloud Support**: AWS, Azure, and GCP integration
- **Cloud Dumps**: Direct analysis of cloud-stored memory dumps
- **Result Upload**: Upload analysis results to cloud storage
- **Scalability**: Handle large cloud-based memory dumps

### 4. Advanced Features
- **Plugin System**: Extensible plugin architecture
- **Error Handling**: Robust error handling and fallback mechanisms
- **Performance Monitoring**: Real-time performance metrics
- **Export Formats**: Multiple output formats (JSON, CSV, XML)

## Installation & Setup

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/memory-forensics-framework.git
cd memory-forensics-framework

# Run setup (choose your platform)
# Windows
.\scripts\setup.ps1

# Linux/macOS
./scripts/setup.sh

# Universal Python
python scripts/setup.py
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install memory forensics tools
pip install volatility3 rekall psutil yara-python

# Run tests
pytest src/tests/ -v
```

## Usage

### Basic Usage
```python
from src.framework.unified_api import MemoryForensicsFramework

# Initialize framework
framework = MemoryForensicsFramework()

# Analyze memory dump
result = framework.analyze_memory_dump("memory.dmp", os_type="windows")

# Export results
framework.export_results(result, "analysis_results.json")
```

### Command Line
```bash
# Analyze memory dump
python -m src.framework.unified_api --dump memory.dmp --os windows

# With semantic analysis
python -m src.framework.unified_api --dump memory.dmp --os windows --semantic

# List available tools
python -m src.framework.unified_api --list-tools
```

## Weekly Progress

### Week 1: Foundation & Literature Review
- ✅ Literature review (15+ papers analyzed)
- ✅ Base paper analysis
- ✅ Tool capability assessment
- ✅ Framework architecture design
- ✅ Initial API specification

### Week 2: Tool Analysis & Framework Design
- ✅ Deep tool analysis (Volatility, Rekall, MemProcFS)
- ✅ Framework architecture refinement
- ✅ API specification completion
- ✅ Extension methodology development

### Week 3: Core Implementation
- ✅ Unified API implementation
- ✅ Tool wrapper development
- ✅ OS detection logic
- ✅ Basic semantic analyzer
- ✅ Cross-platform testing

### Week 4: Advanced Features & Testing
- ✅ Semantic analysis engine
- ✅ Intelligent tool selection
- ✅ Error handling system
- ✅ Performance monitoring
- ✅ Comprehensive testing

### Week 5: Plugin System & Cloud Integration
- ✅ Plugin architecture
- ✅ Cloud handler implementation
- ✅ AWS, Azure, GCP integration
- ✅ Advanced error handling
- ✅ Fallback mechanisms

### Week 6: Performance Optimization & Validation
- ✅ Performance optimization
- ✅ Cross-platform validation
- ✅ Benchmark testing
- ✅ Memory optimization
- ✅ Scalability testing

### Week 7: Documentation & Finalization
- ✅ Complete documentation
- ✅ Final testing
- ✅ Report generation
- ✅ Presentation preparation
- ✅ Project finalization

## Testing

### Run All Tests
```bash
pytest src/tests/ -v
```

### Run Specific Test Suites
```bash
# Framework tests
pytest src/tests/test_framework.py -v

# Tool wrapper tests
pytest src/tests/test_tools.py -v

# Semantic analyzer tests
pytest src/tests/test_semantic.py -v

# Cloud handler tests
pytest src/tests/test_cloud.py -v
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

### User Documentation
- **User Guide**: `docs/guides/user_guide.md`
- **API Documentation**: `docs/guides/api_documentation.md`
- **Technical Specs**: `docs/guides/technical_specs.md`

### Weekly Reports
- **Week 1**: Literature review and foundation analysis
- **Week 2**: Tool analysis and framework design
- **Week 3**: Core implementation and testing
- **Week 4**: Advanced features and comprehensive testing
- **Week 5**: Plugin system and cloud integration
- **Week 6**: Performance optimization and validation
- **Week 7**: Documentation and finalization

### Presentations
- Weekly presentations in `weekX/presentations/`
- Final presentation in `week7/presentations/`

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
