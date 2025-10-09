#!/usr/bin/env python3
"""
Week 1 Analysis Script - Tool Analysis and Testing
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
        logging.FileHandler('week1/logs/analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Week1Analysis:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        self.log_file = self.script_dir / 'logs' / 'validation.log'
        
    def test_tool(self, tool_name, command):
        """Test a memory forensics tool"""
        logger.info(f"Testing {tool_name}...")
        
        try:
            result = subprocess.run(
                [command, '--help'], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            test_result = {
                'tool': tool_name,
                'command': command,
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'timestamp': datetime.now().isoformat()
            }
            
            if result.returncode == 0:
                logger.info(f"{tool_name} test successful")
            else:
                logger.warning(f"{tool_name} test failed: {result.stderr}")
                
            return test_result
            
        except subprocess.TimeoutExpired:
            logger.error(f"{tool_name} test timed out")
            return {
                'tool': tool_name,
                'command': command,
                'success': False,
                'error': 'Timeout',
                'timestamp': datetime.now().isoformat()
            }
        except FileNotFoundError:
            logger.error(f"{tool_name} not found")
            return {
                'tool': tool_name,
                'command': command,
                'success': False,
                'error': 'Tool not found',
                'timestamp': datetime.now().isoformat()
            }
            
    def run_tool_analysis(self):
        """Run analysis on all memory forensics tools"""
        logger.info("Running tool analysis...")
        
        tools = {
            'volatility3': 'vol',
            'rekall': 'rekall',
            'memprocfs': 'memprocfs'
        }
        
        results = []
        
        for tool_name, command in tools.items():
            result = self.test_tool(tool_name, command)
            results.append(result)
            
            # Save individual test log
            log_file = self.script_dir / 'logs' / f'{tool_name}_test.log'
            with open(log_file, 'w') as f:
                f.write(f"Tool: {tool_name}\n")
                f.write(f"Command: {command}\n")
                f.write(f"Success: {result['success']}\n")
                f.write(f"Timestamp: {result['timestamp']}\n")
                if 'stdout' in result:
                    f.write(f"STDOUT:\n{result['stdout']}\n")
                if 'stderr' in result:
                    f.write(f"STDERR:\n{result['stderr']}\n")
                if 'error' in result:
                    f.write(f"Error: {result['error']}\n")
                    
        # Save combined results
        results_file = self.script_dir / 'logs' / 'tool_analysis_results.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        logger.info("Tool analysis completed")
        return results
        
    def generate_tool_matrix(self):
        """Generate tool comparison matrix"""
        logger.info("Generating tool comparison matrix...")
        
        matrix = {
            'tools': ['Volatility3', 'Rekall', 'MemProcFS'],
            'features': [
                'Cross-platform',
                'Plugin ecosystem', 
                'Performance',
                'Documentation',
                'Community',
                'Integration',
                'Cloud support',
                'Memory efficiency'
            ],
            'scores': {
                'Volatility3': [True, True, False, True, True, True, False, False],
                'Rekall': [True, False, True, False, False, False, True, True],
                'MemProcFS': [True, False, True, False, False, False, False, True]
            }
        }
        
        # Save matrix as JSON
        matrix_file = self.script_dir / 'reports' / 'tool_matrix.json'
        with open(matrix_file, 'w') as f:
            json.dump(matrix, f, indent=2)
            
        # Save matrix as CSV
        csv_file = self.script_dir / 'reports' / 'tool_matrix.csv'
        with open(csv_file, 'w') as f:
            f.write("Tool,Cross-platform,Plugin ecosystem,Performance,Documentation,Community,Integration,Cloud support,Memory efficiency\n")
            for tool in matrix['tools']:
                scores = matrix['scores'][tool]
                score_str = ','.join(['1' if score else '0' for score in scores])
                f.write(f"{tool},{score_str}\n")
                
        logger.info("Tool matrix generated")
        return matrix
        
    def run(self):
        """Run Week 1 analysis"""
        logger.info("Starting Week 1 analysis...")
        
        try:
            results = self.run_tool_analysis()
            matrix = self.generate_tool_matrix()
            
            logger.info("Week 1 analysis completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Week 1 analysis failed: {e}")
            return False

if __name__ == "__main__":
    analysis = Week1Analysis()
    success = analysis.run()
    sys.exit(0 if success else 1)
