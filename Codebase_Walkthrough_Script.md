# Codebase Walkthrough Script: Project Defense

**Purpose:** Use this script when showing your code to the professor. It explains *every* file in the project.

---

## 1. Root Directory (Project Context)
**`README.md`**: "This is the entry point documentation. It explains the project's academic background, architecture, and provides quick-start commands for installation and usage."
**`requirements.txt`**: "Lists all Python dependencies. Key libraries are `volatility3` for forensics, `click` for the CLI, and `pytest` for testing."
**`setup.py`**: "This is the package installation script. It defines `unified-forensics` as a system-wide command, allowing us to run the tool from any terminal."

## 2. Core Framework (`unified_forensics/core/`)
**`framework.py`**: "This is the **Heart** of the project. The `UnifiedForensicsFramework` class initializes the tools (Volatility, Rekall) and orchestrates the analysis flow. It decides which tool to use based on the OS."
**`os_detector.py`**: "A utility module. It reads the first few bytes of a memory file (magic headers) or uses file extensions to guess if the dump is Windows, Linux, or Mac."
**`output_standardizer.py`**: "Crucial for unification. It takes the different output formats from Volatility (JSON) and Rekall (text/mixed) and converts them into a single, consistent JSON structure for our plugins."
**`detection_metrics.py`**: "Used for my research experiments. It tracks how long analysis takes and calculates 'Precision' and 'Recall' if we have ground-truth data."
**`experimental_framework.py`**: "Contains the logic for the Research Paper's methodology. It runs the loop that generates the 'Event Rate vs Detection' graphs."

## 3. Tool Wrappers (`unified_forensics/tools/`)
**`volatility_wrapper.py`**: "This class interfaces with the Volatility 3 library. It constructs the command-line arguments (e.g., `windows.pslist`) and parses the raw output."
**`rekall_wrapper.py`**: "Similar to the Volatility wrapper but designed for Rekall commands, primarily used for older Windows updates or macOS support."
**`memprocfs_wrapper.py`**: "An interface for MemProcFS. It's a fallback tool if Volatility fails, allowing us to read memory as a file system."

## 4. Plugins (`unified_forensics/plugins/`)
**`malware_detector.py`**: "The security logic. It takes the standardized process list and checks names against a list of known bad regex patterns (like `nc.exe`, `minerd`)."
**`network_analyzer.py`**: "Analyzes network artifacts. It looks for suspicious ports (like 4444 or 6667) and flags High-Risk connections."

## 5. Automation Scripts (The "How-To")
**`setup_windows.bat` / `setup_linux.sh`**: "These are my one-click setup scripts. They install Python, create a Virtual Environment (`venv`), and install all dependencies automatically."
**`test_complete_malware.bat` / `test_complete_malware.sh`**: "My end-to-end testing scripts. They simulate a malware attack, dump the memory, and run the analysis tool to verify detection, proving the system works."
**`test_malware_simulation.py`**: "A Python script that creates a 'fake' malware process (sleeping process) so we have something safe to detect during demonstrations."
**`create_malware_memory_dump.py`**: "A utility that simulates the creation of a memory dump file for testing purposes."

## 6. Tests (`tests/`)
**`tests/` directory**: "Contains `pytest` unit tests that verify each component in isolation, ensuring the code is robust."
