#!/usr/bin/env python3
"""
Comprehensive test runner for the Unified Memory Forensics Framework
This script runs all tests and generates a complete validation report
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path

def setup_testing_environment():
    """Setup the comprehensive testing environment"""
    print("Setting up comprehensive testing environment...")
    
    # Create necessary directories with descriptive names
    directories = ['memory_dump_samples', 'analysis_results', 'performance_charts', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    print("Testing environment setup complete!\n")

def run_basic_tests():
    """Run basic functionality tests"""
    print("="*60)
    print("RUNNING BASIC FUNCTIONALITY TESTS")
    print("="*60)
    
    try:
        # Test framework import
        result = subprocess.run([sys.executable, '-c', 
                               'from unified_forensics.core.framework import UnifiedForensicsFramework; print("Import successful")'],
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ Framework import test passed")
        else:
            print(f"✗ Framework import test failed: {result.stderr}")
            return False
        
        # Test CLI info command
        result = subprocess.run([sys.executable, '-m', 'unified_forensics', 'info'],
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ CLI info command test passed")
        else:
            print(f"✗ CLI info command test failed: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Basic tests failed with error: {str(e)}")
        return False

def generate_memory_dump_samples():
    """Generate memory dump samples for all platforms"""
    print("\n" + "="*60)
    print("GENERATING MEMORY DUMP SAMPLES")
    print("="*60)
    
    try:
        # Generate memory dump samples for all platforms
        result = subprocess.run([sys.executable, 'memory_dump_generator.py', 'all'],
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✓ Memory dump sample generation completed")
            print("Generated memory dump samples:")
            for file in os.listdir('memory_dump_samples'):
                if file.endswith('.mem'):
                    size = os.path.getsize(f'memory_dump_samples/{file}') / (1024*1024)
                    print(f"  - {file} ({size:.1f} MB)")
            return True
        else:
            print(f"✗ Memory dump sample generation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Memory dump sample generation failed with error: {str(e)}")
        return False

def run_memory_analysis_tests():
    """Run comprehensive memory analysis tests"""
    print("\n" + "="*60)
    print("RUNNING MEMORY ANALYSIS TESTS")
    print("="*60)
    
    memory_sample_files = []
    for file in os.listdir('memory_dump_samples'):
        if file.endswith('.mem'):
            memory_sample_files.append(f'memory_dump_samples/{file}')
    
    if not memory_sample_files:
        print("✗ No memory sample files found")
        return False
    
    successful_analyses = 0
    for sample_file in memory_sample_files:
        print(f"Analyzing: {sample_file}")
        
        try:
            # Run comprehensive memory analysis
            result = subprocess.run([sys.executable, '-m', 'unified_forensics', 'analyze', 
                                   sample_file, '--format', 'summary'],
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"  ✓ Memory analysis successful")
                successful_analyses += 1
            else:
                print(f"  ✗ Memory analysis failed: {result.stderr}")
                
        except Exception as e:
            print(f"  ✗ Memory analysis failed with error: {str(e)}")
    
    print(f"\nMemory analysis tests: {successful_analyses}/{len(memory_sample_files)} passed")
    return successful_analyses == len(memory_sample_files)

def run_experimental_tests():
    """Run experimental analysis tests"""
    print("\n" + "="*60)
    print("RUNNING EXPERIMENTAL ANALYSIS TESTS")
    print("="*60)
    
    test_files = []
    for file in os.listdir('test_data'):
        if file.endswith('.mem'):
            test_files.append(f'test_data/{file}')
    
    if not test_files:
        print("✗ No test files found")
        return False
    
    success_count = 0
    for test_file in test_files:
        print(f"Running experimental analysis: {test_file}")
        
        try:
            # Determine OS type from filename
            if 'windows' in test_file:
                os_type = 'windows'
            elif 'linux' in test_file:
                os_type = 'linux'
            elif 'macos' in test_file:
                os_type = 'macos'
            else:
                os_type = 'windows'  # default
            
            # Run experimental analysis with limited event rates for speed
            result = subprocess.run([sys.executable, '-m', 'unified_forensics', 'experiment',
                                   test_file, '--os', os_type, '--rates', '1', '--rates', '10',
                                   '--output', f'test_results/experimental_{os_type}_{int(time.time())}.json'],
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"  ✓ Experimental analysis successful")
                success_count += 1
            else:
                print(f"  ✗ Experimental analysis failed: {result.stderr}")
                
        except Exception as e:
            print(f"  ✗ Experimental analysis failed with error: {str(e)}")
    
    print(f"\nExperimental tests: {success_count}/{len(test_files)} passed")
    return success_count == len(test_files)

def run_cross_platform_validation():
    """Run cross-platform validation tests"""
    print("\n" + "="*60)
    print("RUNNING CROSS-PLATFORM VALIDATION")
    print("="*60)
    
    test_dumps = {}
    for file in os.listdir('test_data'):
        if file.endswith('.mem'):
            if 'windows' in file:
                test_dumps['windows'] = f'test_data/{file}'
            elif 'linux' in file:
                test_dumps['linux'] = f'test_data/{file}'
            elif 'macos' in file:
                test_dumps['macos'] = f'test_data/{file}'
    
    if not test_dumps:
        print("✗ No test dumps found for cross-platform validation")
        return False
    
    try:
        # Build validation command
        cmd = [sys.executable, '-m', 'unified_forensics', 'validate']
        for platform, dump_file in test_dumps.items():
            cmd.extend([f'--{platform}-dump', dump_file])
        cmd.extend(['--output', f'test_results/cross_platform_validation_{int(time.time())}.json'])
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✓ Cross-platform validation successful")
            return True
        else:
            print(f"✗ Cross-platform validation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Cross-platform validation failed with error: {str(e)}")
        return False

def generate_final_report(test_results):
    """Generate final comprehensive test report"""
    print("\n" + "="*60)
    print("GENERATING FINAL REPORT")
    print("="*60)
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'framework_version': '1.0.0',
        'test_environment': {
            'python_version': sys.version,
            'platform': sys.platform,
            'working_directory': os.getcwd()
        },
        'test_results': test_results,
        'summary': {
            'total_tests': len(test_results),
            'passed_tests': sum(1 for result in test_results.values() if result),
            'failed_tests': sum(1 for result in test_results.values() if not result),
            'success_rate': f"{(sum(1 for result in test_results.values() if result) / len(test_results)) * 100:.1f}%"
        },
        'files_generated': {
            'test_data': list(os.listdir('test_data')) if os.path.exists('test_data') else [],
            'test_results': list(os.listdir('test_results')) if os.path.exists('test_results') else [],
            'test_images': list(os.listdir('test_images')) if os.path.exists('test_images') else []
        }
    }
    
    # Save report
    report_file = f'test_results/comprehensive_test_report_{int(time.time())}.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Final report generated: {report_file}")
    return report

def main():
    """Main test runner function"""
    print("UNIFIED MEMORY FORENSICS FRAMEWORK - COMPREHENSIVE TEST RUNNER")
    print("="*80)
    
    # Setup comprehensive testing environment
    setup_testing_environment()
    
    # Run all comprehensive tests
    test_results = {}
    
    test_results['basic_functionality'] = run_basic_tests()
    test_results['memory_dump_generation'] = generate_memory_dump_samples()
    test_results['memory_analysis'] = run_memory_analysis_tests()
    test_results['experimental_analysis'] = run_experimental_tests()
    test_results['cross_platform_validation'] = run_cross_platform_validation()
    
    # Generate final report
    report = generate_final_report(test_results)
    
    # Display final results
    print("\n" + "="*80)
    print("FINAL TEST RESULTS")
    print("="*80)
    
    for test_name, result in test_results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    print("-" * 80)
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed_tests']}")
    print(f"Failed: {report['summary']['failed_tests']}")
    print(f"Success Rate: {report['summary']['success_rate']}")
    
    if report['summary']['failed_tests'] == 0:
        print("\n🎉 ALL TESTS PASSED! Framework is ready for production use.")
        return 0
    else:
        print(f"\n⚠️  {report['summary']['failed_tests']} test(s) failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
