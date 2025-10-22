# User Guide

## Quick Start

### Basic Analysis

The simplest way to analyze a memory dump:

```bash
unified-forensics analyze memory_dump.mem
```

### Specify Operating System

If you know the operating system:

```bash
unified-forensics analyze memory_dump.mem --os windows
```

### Save Results

Save results to a file:

```bash
unified-forensics analyze memory_dump.mem --output results.json
```

### Use Plugins

Enable specific plugins for enhanced analysis:

```bash
unified-forensics analyze memory_dump.mem --plugins malware,network
```

## Command Reference

### Main Commands

#### `analyze`
Analyze a memory dump file.

**Syntax:**
```bash
unified-forensics analyze <memory_dump> [OPTIONS]
```

**Arguments:**
- `memory_dump`: Path to the memory dump file

**Options:**
- `--os, -o`: Specify operating system (windows, linux, macos)
- `--output, -f`: Output file for results
- `--plugins, -p`: Enable specific plugins (multiple allowed)
- `--format`: Output format (json, table, summary)
- `--verbose, -v`: Enable verbose logging
- `--debug, -d`: Enable debug logging

**Examples:**
```bash
# Basic analysis
unified-forensics analyze dump.mem

# Windows analysis with malware detection
unified-forensics analyze dump.mem --os windows --plugins malware

# Save results to file
unified-forensics analyze dump.mem --output results.json

# Table format output
unified-forensics analyze dump.mem --format table

# Verbose logging
unified-forensics analyze dump.mem --verbose
```

#### `info`
Display framework information.

**Syntax:**
```bash
unified-forensics info
```

**Output:**
- Supported operating systems
- Available tools
- Available plugins
- Framework version

#### `detect-os`
Detect operating system from memory dump.

**Syntax:**
```bash
unified-forensics detect-os <memory_dump>
```

**Arguments:**
- `memory_dump`: Path to the memory dump file

## Output Formats

### JSON Format (Default)
Structured JSON output with complete analysis results:

```json
{
  "metadata": {
    "os_type": "windows",
    "analysis_timestamp": "2025-01-15T10:30:00",
    "framework_version": "1.0.0"
  },
  "processes": [
    {
      "pid": 1234,
      "name": "notepad.exe",
      "parent_pid": 5678,
      "command_line": "notepad test.txt",
      "suspicious": false
    }
  ],
  "network_connections": [
    {
      "local_address": "127.0.0.1",
      "local_port": 8080,
      "remote_address": "192.168.1.1",
      "remote_port": 80,
      "protocol": "tcp",
      "state": "ESTABLISHED"
    }
  ],
  "statistics": {
    "total_processes": 50,
    "total_network_connections": 10,
    "suspicious_processes": 2
  }
}
```

### Table Format
Human-readable table output:

```
=== ANALYSIS RESULTS ===
OS Type: windows
Analysis Time: 2025-01-15T10:30:00

Processes (50):
  [NORMAL] PID: 1234 | Name: notepad.exe
  [SUSPICIOUS] PID: 5678 | Name: cmd.exe
  ... and 48 more processes

Network Connections (10):
  127.0.0.1:8080 -> 192.168.1.1:80
  192.168.1.1:443 -> 8.8.8.8:443
  ... and 8 more connections

Statistics:
  Total Processes: 50
  Total Connections: 10
  Suspicious Processes: 2
  Active Connections: 5
```

### Summary Format
Brief summary of key findings:

```
=== ANALYSIS SUMMARY ===
OS Type: windows
Total Processes: 50
Total Connections: 10
Suspicious Processes: 2
⚠️  Suspicious activity detected!
```

## Plugins

### Malware Detector Plugin

Detects suspicious processes and malware indicators.

**Features:**
- Suspicious process detection
- Command line analysis
- Malware pattern matching
- Confidence scoring

**Usage:**
```bash
unified-forensics analyze dump.mem --plugins malware
```

**Output:**
```json
{
  "plugin_results": {
    "malware_detector": {
      "malware_indicators": [
        {
          "type": "suspicious_process",
          "process_name": "cmd.exe",
          "command_line": "cmd /c powershell -enc base64",
          "pattern_matched": "cmd\\.exe",
          "confidence": 0.8
        }
      ],
      "suspicious_processes": [
        {
          "pid": 1234,
          "name": "cmd.exe",
          "command_line": "cmd /c powershell -enc base64",
          "suspicious_score": 0.8,
          "reasons": ["PowerShell usage", "Base64 encoding"]
        }
      ],
      "confidence_score": 0.8,
      "threat_level": "high"
    }
  }
}
```

### Network Analyzer Plugin

Analyzes network connections and detects suspicious activity.

**Features:**
- Suspicious port detection
- IP address analysis
- Connection pattern analysis
- Threat indicator detection

**Usage:**
```bash
unified-forensics analyze dump.mem --plugins network
```

**Output:**
```json
{
  "plugin_results": {
    "network_analyzer": {
      "suspicious_connections": [
        {
          "connection": {
            "local_address": "127.0.0.1",
            "local_port": 8080,
            "remote_address": "192.168.1.1",
            "remote_port": 22
          },
          "reason": "Suspicious port 22",
          "severity": "medium"
        }
      ],
      "port_analysis": {
        "most_used_ports": [[80, 5], [443, 3], [22, 1]],
        "suspicious_ports": [22],
        "total_unique_ports": 3
      },
      "threat_indicators": [
        {
          "type": "potential_backdoor",
          "port": 22,
          "address": "192.168.1.1",
          "severity": "high"
        }
      ]
    }
  }
}
```

## Advanced Usage

### Custom Analysis

For programmatic usage:

```python
from unified_forensics import UnifiedForensicsFramework

# Initialize framework
framework = UnifiedForensicsFramework()

# Analyze memory dump
results = framework.analyze(
    memory_dump_path='dump.mem',
    os_type='windows',
    plugins=['malware', 'network'],
    output_file='results.json'
)

# Access results
processes = results['processes']
network = results['network_connections']
statistics = results['statistics']
```

### Batch Analysis

Analyze multiple memory dumps:

```bash
#!/bin/bash
for dump in dumps/*.mem; do
    echo "Analyzing $dump"
    unified-forensics analyze "$dump" --output "results/$(basename "$dump").json"
done
```

### Integration with Other Tools

The framework can be integrated with other forensic tools:

```python
import subprocess
import json

# Run framework analysis
result = subprocess.run([
    'unified-forensics', 'analyze', 'dump.mem',
    '--output', 'results.json'
], capture_output=True, text=True)

# Load results
with open('results.json', 'r') as f:
    results = json.load(f)

# Process results
for process in results['processes']:
    if process['suspicious']:
        print(f"Suspicious process: {process['name']}")
```

## Troubleshooting

### Common Issues

#### 1. Tool Not Found
```
Error: Tool 'volatility' not found
```

**Solution:**
- Install the required tools
- Check PATH environment variable
- Use absolute paths to tools

#### 2. Memory Dump Format
```
Error: Unsupported memory dump format
```

**Solution:**
- Ensure dump is in supported format (.mem, .dmp, .vmem)
- Check file integrity
- Try different OS detection

#### 3. Permission Issues
```
Error: Permission denied
```

**Solution:**
- Run with appropriate permissions
- Check file ownership
- Use sudo if necessary

#### 4. Plugin Errors
```
Error: Plugin 'malware' failed
```

**Solution:**
- Check plugin installation
- Review error logs
- Try without plugins first

### Debug Mode

Enable debug mode for detailed logging:

```bash
unified-forensics analyze dump.mem --debug
```

### Log Files

Check log files for detailed error information:

```bash
# Check system logs
tail -f /var/log/syslog  # Linux
Get-EventLog -LogName Application  # Windows
log show --predicate 'process == "unified-forensics"'  # macOS
```

## Performance Tips

### Optimization

1. **Use SSD storage** for faster I/O
2. **Increase RAM** for large memory dumps
3. **Close unnecessary applications** during analysis
4. **Use specific OS detection** instead of auto-detection
5. **Disable plugins** if not needed

### Resource Usage

- **CPU**: High during analysis
- **Memory**: 2-4GB for typical dumps
- **Storage**: 1-2GB for results
- **Time**: 5-30 minutes depending on dump size

## Best Practices

### Security

1. **Use isolated environments** for analysis
2. **Never analyze production systems** directly
3. **Encrypt sensitive results**
4. **Follow chain of custody** procedures
5. **Document all analysis steps**

### Analysis

1. **Start with basic analysis** before using plugins
2. **Verify results** with multiple tools
3. **Document findings** thoroughly
4. **Keep original dumps** for verification
5. **Use version control** for analysis scripts

### Maintenance

1. **Update tools regularly**
2. **Backup configurations**
3. **Monitor disk space**
4. **Review logs periodically**
5. **Test after updates**
