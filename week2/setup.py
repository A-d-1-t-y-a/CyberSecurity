#!/usr/bin/env python3
"""
Week 2 Setup Script - Deep Tool Analysis and Framework Design
Cross-Platform Unified Memory Forensics Framework
Student: Manoj Santhoju (ID: 23394544)
Institution: National College of Ireland
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
import json
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('week2/logs/setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week2Setup:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.log_file = self.script_dir / 'logs' / 'validation.log'
        
    def setup_directories(self):
        """Create necessary directories for Week 2"""
        logger.info("Setting up Week 2 directories...")
        
        directories = [
            'week2/logs',
            'week2/data', 
            'week2/reports',
            'week2/presentations',
            'week2/code',
            'docs/architecture',
            'docs/api_specs'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
            
    def install_advanced_dependencies(self):
        """Install advanced dependencies for Week 2"""
        logger.info("Installing advanced dependencies...")
        
        advanced_deps = [
            'plantuml',  # For architecture diagrams
            'matplotlib',  # For plotting
            'seaborn',  # For statistical plots
            'pydot',  # For graph visualization
            'graphviz',  # For diagram generation
            'jsonschema',  # For API validation
            'pydantic',  # For data validation
            'fastapi',  # For API development
            'uvicorn'  # For API server
        ]
        
        for dep in advanced_deps:
            try:
                subprocess.run([
                    sys.executable, '-m', 'pip', 'install', 
                    dep, '--user'
                ], check=True, capture_output=True)
                logger.info(f"Installed {dep}")
            except subprocess.CalledProcessError:
                logger.warning(f"Failed to install {dep}")
                
    def generate_architecture_diagrams(self):
        """Generate architecture diagrams using PlantUML"""
        logger.info("Generating architecture diagrams...")
        
        # Create PlantUML files
        plantuml_files = {
            'framework_architecture.puml': self._get_framework_architecture_puml(),
            'api_design.puml': self._get_api_design_puml(),
            'tool_integration.puml': self._get_tool_integration_puml(),
            'data_flow.puml': self._get_data_flow_puml()
        }
        
        diagrams_dir = self.project_root / 'docs' / 'architecture'
        
        for filename, content in plantuml_files.items():
            file_path = diagrams_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Generated {filename}")
            
    def _get_framework_architecture_puml(self):
        """Generate PlantUML for framework architecture"""
        return """@startuml Framework Architecture
!theme plain

title Cross-Platform Unified Memory Forensics Framework Architecture

package "Unified API Layer" {
    [MemoryForensicsFramework] as MFF
    [ConfigurationManager] as CM
    [ErrorHandler] as EH
}

package "Tool Wrapper Layer" {
    [VolatilityWrapper] as VW
    [RekallWrapper] as RW
    [MemProcFSWrapper] as MW
}

package "Semantic Analysis Layer" {
    [SemanticAnalyzer] as SA
    [PatternRecognizer] as PR
    [ThreatDetector] as TD
}

package "OS Detection Layer" {
    [OSDetector] as OD
    [ToolSelector] as TS
}

package "Cloud Handler Layer" {
    [CloudHandler] as CH
    [AWSProvider] as AWS
    [AzureProvider] as AZ
    [GCPProvider] as GCP
}

MFF --> VW
MFF --> RW
MFF --> MW
MFF --> SA
MFF --> OD
MFF --> CH

SA --> PR
SA --> TD

OD --> TS

CH --> AWS
CH --> AZ
CH --> GCP

@enduml"""
        
    def _get_api_design_puml(self):
        """Generate PlantUML for API design"""
        return """@startuml API Design
!theme plain

title Unified API Design

interface MemoryForensicsFramework {
    + analyze_memory_dump(dump_path: str, os_type: str) -> AnalysisResult
    + export_results(results: AnalysisResult, output_path: str) -> bool
    + get_available_tools() -> List[str]
    + get_tool_capabilities(tool: str) -> Dict[str, Any]
}

interface BaseToolWrapper {
    + execute_command(command: str, args: List[str]) -> CommandResult
    + parse_output(output: str) -> ParsedOutput
    + get_plugins() -> List[str]
}

class VolatilityWrapper {
    + analyze_dump(dump_path: str, plugin: str) -> VolatilityResult
    + list_plugins() -> List[str]
}

class RekallWrapper {
    + analyze_dump(dump_path: str, plugin: str) -> RekallResult
    + list_plugins() -> List[str]
}

class MemProcFSWrapper {
    + analyze_dump(dump_path: str, plugin: str) -> MemProcFSResult
    + list_plugins() -> List[str]
}

MemoryForensicsFramework --> BaseToolWrapper
BaseToolWrapper <|-- VolatilityWrapper
BaseToolWrapper <|-- RekallWrapper
BaseToolWrapper <|-- MemProcFSWrapper

@enduml"""
        
    def _get_tool_integration_puml(self):
        """Generate PlantUML for tool integration"""
        return """@startuml Tool Integration
!theme plain

title Tool Integration Architecture

package "Memory Forensics Tools" {
    [Volatility3] as V3
    [Rekall] as R
    [MemProcFS] as M
}

package "Unified Framework" {
    [ToolManager] as TM
    [OutputStandardizer] as OS
    [ResultAggregator] as RA
}

package "Analysis Results" {
    [StandardizedOutput] as SO
    [SemanticAnalysis] as SA
    [ThreatIndicators] as TI
}

V3 --> TM
R --> TM
M --> TM

TM --> OS
OS --> RA
RA --> SO
RA --> SA
RA --> TI

@enduml"""
        
    def _get_data_flow_puml(self):
        """Generate PlantUML for data flow"""
        return """@startuml Data Flow
!theme plain

title Data Flow Architecture

start

:Memory Dump Input;
:OS Detection;
:Tool Selection;
:Tool Execution;
:Output Parsing;
:Semantic Analysis;
:Result Aggregation;
:Standardized Output;

stop

@enduml"""
        
    def create_api_specifications(self):
        """Create detailed API specifications"""
        logger.info("Creating API specifications...")
        
        api_spec = {
            "framework": {
                "name": "MemoryForensicsFramework",
                "version": "1.0.0",
                "description": "Unified memory forensics framework",
                "methods": {
                    "analyze_memory_dump": {
                        "parameters": ["dump_path", "os_type", "options"],
                        "returns": "AnalysisResult",
                        "description": "Analyze memory dump using appropriate tool"
                    },
                    "export_results": {
                        "parameters": ["results", "output_path", "format"],
                        "returns": "bool",
                        "description": "Export analysis results to file"
                    },
                    "get_available_tools": {
                        "parameters": [],
                        "returns": "List[str]",
                        "description": "Get list of available tools"
                    }
                }
            },
            "tool_wrappers": {
                "base_class": "BaseToolWrapper",
                "implementations": ["VolatilityWrapper", "RekallWrapper", "MemProcFSWrapper"],
                "common_methods": ["execute_command", "parse_output", "get_plugins"]
            },
            "semantic_analysis": {
                "analyzer": "SemanticAnalyzer",
                "components": ["PatternRecognizer", "ThreatDetector", "BehaviorClassifier"],
                "output_format": "JSON with semantic tags"
            }
        }
        
        api_spec_file = self.project_root / 'docs' / 'api_specs' / 'api_specification.json'
        with open(api_spec_file, 'w', encoding='utf-8') as f:
            json.dump(api_spec, f, indent=2)
            
        logger.info("API specifications created")
        
    def run(self):
        """Run Week 2 setup"""
        logger.info("Starting Week 2 setup...")
        
        try:
            self.setup_directories()
            self.install_advanced_dependencies()
            self.generate_architecture_diagrams()
            self.create_api_specifications()
            
            logger.info("Week 2 setup completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Week 2 setup failed: {e}")
            return False

if __name__ == "__main__":
    setup = Week2Setup()
    success = setup.run()
    sys.exit(0 if success else 1)
