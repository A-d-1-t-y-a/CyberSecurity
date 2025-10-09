# Memory Forensics Framework User Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [API Reference](#api-reference)
6. [Troubleshooting](#troubleshooting)
7. [Examples](#examples)

## Installation

### Prerequisites
- Python 3.9+
- 8GB+ RAM (recommended)
- 50GB+ free disk space
- Windows 11, Ubuntu 22.04+, or macOS Ventura

### Quick Installation

#### Windows
```powershell
# Run PowerShell setup script
.\scripts\setup.ps1

# Or use Python setup
python scripts\setup.py
```

#### Linux/macOS
```bash
# Run bash setup script
./scripts/setup.sh

# Or use Python setup
python3 scripts/setup.py
```

#### Universal Python Setup
```bash
# Works on all platforms
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

## Quick Start

### 1. Initialize Framework
```python
from src.framework.unified_api import MemoryForensicsFramework

# Create framework instance
framework = MemoryForensicsFramework()

# Check framework status
info = framework.get_framework_info()
print(f"Framework: {info['name']} v{info['version']}")
print(f"Available tools: {[k for k, v in info['available_tools'].items() if v]}")
```

### 2. Analyze Memory Dump
```python
# Analyze memory dump
result = framework.analyze_memory_dump(
    "memory.dmp",
    os_type="windows",
    use_semantic=True
)

print(f"Analysis completed using {result['tool_used']}")
print(f"Execution time: {result['execution_time']:.2f} seconds")
```

### 3. Export Results
```python
# Export results to JSON
framework.export_results(result, "analysis_results.json", "json")

# Export results to CSV
framework.export_results(result, "analysis_results.csv", "csv")
```

## Basic Usage

### Command Line Interface

#### Analyze Memory Dump
```bash
# Basic analysis
python -m src.framework.unified_api --dump memory.dmp --os windows

# With semantic analysis
python -m src.framework.unified_api --dump memory.dmp --os windows --semantic

# Specify output file
python -m src.framework.unified_api --dump memory.dmp --os windows --output results.json
```

#### List Available Tools
```bash
python -m src.framework.unified_api --list-tools
```

#### Show Framework Info
```bash
python -m src.framework.unified_api --info
```

### Python API Usage

#### Basic Analysis
```python
from src.framework.unified_api import MemoryForensicsFramework

framework = MemoryForensicsFramework()

# Analyze with automatic OS detection
result = framework.analyze_memory_dump("memory.dmp")

# Analyze with specific OS
result = framework.analyze_memory_dump("memory.dmp", os_type="windows")

# Analyze with specific analysis type
result = framework.analyze_memory_dump(
    "memory.dmp", 
    os_type="windows",
    analysis_type="malware"
)
```

#### Tool Selection
```python
# Get available tools
info = framework.get_framework_info()
available_tools = info['available_tools']

# Select tool manually
selected_tool = framework.select_tool("windows", "process")
print(f"Selected tool: {selected_tool}")
```

#### Plugin Usage
```python
# Get available plugins for a tool
plugins = framework.get_available_plugins("volatility")
print(f"Available plugins: {plugins}")

# Run specific plugin
plugin_result = framework.run_plugin(
    "memory.dmp",
    "volatility",
    "pslist"
)
```

## Advanced Features

### Semantic Analysis

#### Enable Semantic Analysis
```python
# Analyze with semantic analysis
result = framework.analyze_memory_dump(
    "memory.dmp",
    os_type="windows",
    use_semantic=True
)

# Access semantic results
if "semantic_analysis" in result["analysis_results"]:
    semantic = result["analysis_results"]["semantic_analysis"]
    print(f"Semantic score: {semantic['semantic_score']:.2f}")
    print(f"Threat indicators: {len(semantic['threat_indicators'])}")
    print(f"Recommendations: {semantic['recommendations']}")
```

#### Custom Semantic Patterns
```python
from src.framework.semantic_analyzer import SemanticAnalyzer

analyzer = SemanticAnalyzer()

# Analyze specific results
semantic_results = analyzer.analyze(analysis_results, "windows")
print(f"Categories analyzed: {list(semantic_results['categories'].keys())}")
```

### Cloud Integration

#### Analyze Cloud Memory Dumps
```python
# Analyze AWS S3 dump
result = framework.analyze_memory_dump(
    "s3://bucket/memory.dmp",
    cloud_source="aws"
)

# Analyze Azure Blob dump
result = framework.analyze_memory_dump(
    "container/memory.dmp",
    cloud_source="azure"
)

# Analyze GCP Storage dump
result = framework.analyze_memory_dump(
    "bucket/memory.dmp",
    cloud_source="gcp"
)
```

#### Upload Results to Cloud
```python
from src.framework.cloud_handler import CloudHandler

cloud_handler = CloudHandler()

# Upload to AWS S3
success = cloud_handler.upload_results(
    "results.json",
    "aws://bucket/results.json"
)

# Upload to Azure Blob
success = cloud_handler.upload_results(
    "results.json",
    "azure://container/results.json"
)
```

### Cross-Platform Analysis

#### Windows Analysis
```python
# Windows-specific analysis
result = framework.analyze_memory_dump(
    "windows_memory.dmp",
    os_type="windows",
    analysis_type="comprehensive"
)
```

#### Linux Analysis
```python
# Linux-specific analysis
result = framework.analyze_memory_dump(
    "linux_memory.dmp",
    os_type="linux",
    analysis_type="process"
)
```

#### macOS Analysis
```python
# macOS-specific analysis
result = framework.analyze_memory_dump(
    "macos_memory.dmp",
    os_type="macos",
    analysis_type="network"
)
```

## API Reference

### MemoryForensicsFramework Class

#### Methods

##### `__init__(config_path=None)`
Initialize the framework.

**Parameters:**
- `config_path` (str, optional): Path to configuration file

##### `analyze_memory_dump(memory_dump_path, os_type=None, analysis_type="comprehensive", use_semantic=True, cloud_source=None)`
Analyze a memory dump.

**Parameters:**
- `memory_dump_path` (str): Path to memory dump file
- `os_type` (str, optional): Operating system type
- `analysis_type` (str): Type of analysis to perform
- `use_semantic` (bool): Whether to use semantic analysis
- `cloud_source` (str, optional): Cloud source if analyzing cloud dump

**Returns:**
- `Dict[str, Any]`: Analysis results

##### `detect_os(memory_dump_path)`
Detect operating system from memory dump.

**Parameters:**
- `memory_dump_path` (str): Path to memory dump file

**Returns:**
- `str`: Detected operating system

##### `select_tool(os_type, analysis_type="process")`
Select the best tool for the given OS and analysis type.

**Parameters:**
- `os_type` (str): Target operating system
- `analysis_type` (str): Type of analysis to perform

**Returns:**
- `str`: Selected tool name

##### `export_results(results, output_path, format="json")`
Export analysis results to file.

**Parameters:**
- `results` (Dict[str, Any]): Analysis results
- `output_path` (str): Output file path
- `format` (str): Export format (json, csv, xml)

**Returns:**
- `bool`: Success status

##### `get_framework_info()`
Get framework information and status.

**Returns:**
- `Dict[str, Any]`: Framework information

### Analysis Types

#### Available Analysis Types
- `"comprehensive"`: Full analysis with all plugins
- `"process"`: Process-focused analysis
- `"network"`: Network-focused analysis
- `"files"`: File system analysis
- `"malware"`: Malware detection analysis

### Output Formats

#### JSON Format
```json
{
  "status": "success",
  "memory_dump": "memory.dmp",
  "os_type": "windows",
  "tool_used": "volatility",
  "execution_time": 2.5,
  "analysis_results": {
    "plugins": {
      "pslist": {
        "status": "success",
        "output": "..."
      }
    },
    "semantic_analysis": {
      "semantic_score": 0.75,
      "threat_indicators": [...],
      "recommendations": [...]
    }
  }
}
```

#### CSV Format
Results are flattened into CSV format with columns for each field.

## Troubleshooting

### Common Issues

#### 1. Tool Not Found
**Error:** `Tool not found: volatility`

**Solution:**
```bash
# Install Volatility
pip install volatility3

# Verify installation
vol --help
```

#### 2. Memory Dump Not Found
**Error:** `Memory dump file not found`

**Solution:**
- Check file path is correct
- Ensure file exists and is readable
- Use absolute path if relative path fails

#### 3. Permission Denied
**Error:** `Permission denied`

**Solution:**
- Run with appropriate permissions
- Check file ownership
- Use administrator/sudo if needed

#### 4. Timeout Errors
**Error:** `Plugin execution timed out`

**Solution:**
- Increase timeout in configuration
- Use smaller memory dumps for testing
- Check system resources

### Debug Mode

#### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

framework = MemoryForensicsFramework()
```

#### Verbose Output
```bash
# Enable verbose output
python -m src.framework.unified_api --dump memory.dmp --os windows -v
```

### Performance Optimization

#### Large Memory Dumps
- Use SSD storage for better I/O performance
- Increase system RAM
- Use analysis type "process" for faster analysis
- Consider splitting large dumps

#### Network Analysis
- Use "network" analysis type for network-focused analysis
- Enable semantic analysis for better pattern recognition
- Use cloud processing for very large dumps

## Examples

### Example 1: Basic Windows Analysis
```python
from src.framework.unified_api import MemoryForensicsFramework

# Initialize framework
framework = MemoryForensicsFramework()

# Analyze Windows memory dump
result = framework.analyze_memory_dump(
    "windows_memory.dmp",
    os_type="windows",
    analysis_type="comprehensive",
    use_semantic=True
)

# Print results
print(f"Tool used: {result['tool_used']}")
print(f"Execution time: {result['execution_time']:.2f} seconds")

# Export results
framework.export_results(result, "windows_analysis.json")
```

### Example 2: Malware Analysis
```python
# Analyze for malware indicators
result = framework.analyze_memory_dump(
    "suspicious_memory.dmp",
    os_type="windows",
    analysis_type="malware",
    use_semantic=True
)

# Check for threat indicators
if "semantic_analysis" in result["analysis_results"]:
    semantic = result["analysis_results"]["semantic_analysis"]
    threats = semantic["threat_indicators"]
    
    if threats:
        print(f"⚠️  {len(threats)} threat indicators found:")
        for threat in threats:
            print(f"  - {threat['indicator']} ({threat['severity']})")
    else:
        print("✅ No threat indicators found")
```

### Example 3: Cross-Platform Analysis
```python
import os

# Analyze multiple memory dumps
dumps = [
    ("windows_memory.dmp", "windows"),
    ("linux_memory.dmp", "linux"),
    ("macos_memory.dmp", "macos")
]

results = []

for dump_path, os_type in dumps:
    if os.path.exists(dump_path):
        result = framework.analyze_memory_dump(dump_path, os_type)
        results.append(result)
        
        # Export individual results
        output_file = f"{os_type}_analysis.json"
        framework.export_results(result, output_file)
        print(f"✅ {os_type} analysis saved to {output_file}")

# Summary
print(f"\n📊 Analysis Summary:")
print(f"Total dumps analyzed: {len(results)}")
print(f"Successful analyses: {len([r for r in results if r['status'] == 'success'])}")
```

### Example 4: Batch Processing
```python
import glob
from pathlib import Path

# Process all memory dumps in a directory
dump_dir = Path("memory_dumps")
dump_files = list(dump_dir.glob("*.dmp"))

for dump_file in dump_files:
    print(f"Processing {dump_file.name}...")
    
    try:
        result = framework.analyze_memory_dump(str(dump_file))
        
        if result["status"] == "success":
            # Export results
            output_file = f"results/{dump_file.stem}_analysis.json"
            framework.export_results(result, output_file)
            print(f"✅ Saved to {output_file}")
        else:
            print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error processing {dump_file.name}: {e}")
```

## Support

For additional help and support:

1. **Documentation**: Check the complete documentation in `docs/`
2. **Issues**: Report issues on the project repository
3. **Examples**: See more examples in `examples/` directory
4. **Tests**: Run tests to verify installation: `pytest src/tests/ -v`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
