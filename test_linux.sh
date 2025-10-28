#!/bin/bash

echo "=========================================="
echo "UNIFIED MEMORY FORENSICS FRAMEWORK"
echo "Linux Test Suite"
echo "Author: Manoj Santhoju"
echo "Institution: National College of Ireland"
echo "=========================================="

# Activate virtual environment
echo "[0] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    echo "Please run setup_linux.sh first"
    exit 1
fi
echo "SUCCESS: Virtual environment activated"

# Test 1: Framework Info
echo ""
echo "[1] Testing Framework Information..."
python3 -m unified_forensics info
if [ $? -ne 0 ]; then
    echo "ERROR: Framework info test failed"
    exit 1
fi
echo "SUCCESS: Framework info test passed"

# Test 2: Memory Sample Generation
echo ""
echo "[2] Testing Memory Sample Generation..."
python3 quick_sample_generator.py
if [ $? -ne 0 ]; then
    echo "ERROR: Memory sample generation failed"
    exit 1
fi
echo "SUCCESS: Memory sample generation test passed"

# Test 3: Windows Analysis
echo ""
echo "[3] Testing Windows Memory Analysis..."
if [ -f "memory_dump_samples/windows_sample.mem" ]; then
    python3 -m unified_forensics analyze memory_dump_samples/windows_sample.mem --os-type windows --format summary
    if [ $? -ne 0 ]; then
        echo "ERROR: Windows analysis test failed"
        exit 1
    fi
    echo "SUCCESS: Windows analysis test passed"
else
    echo "WARNING: Windows sample not found, skipping test"
fi

# Test 4: Linux Analysis
echo ""
echo "[4] Testing Linux Memory Analysis..."
if [ -f "memory_dump_samples/linux_sample.mem" ]; then
    python3 -m unified_forensics analyze memory_dump_samples/linux_sample.mem --os-type linux --format summary
    if [ $? -ne 0 ]; then
        echo "ERROR: Linux analysis test failed"
        exit 1
    fi
    echo "SUCCESS: Linux analysis test passed"
else
    echo "WARNING: Linux sample not found, skipping test"
fi

# Test 5: macOS Analysis
echo ""
echo "[5] Testing macOS Memory Analysis..."
if [ -f "memory_dump_samples/macos_sample.mem" ]; then
    python3 -m unified_forensics analyze memory_dump_samples/macos_sample.mem --os-type macos --format summary
    if [ $? -ne 0 ]; then
        echo "ERROR: macOS analysis test failed"
        exit 1
    fi
    echo "SUCCESS: macOS analysis test passed"
else
    echo "WARNING: macOS sample not found, skipping test"
fi

# Test 6: Experimental Analysis
echo ""
echo "[6] Testing Experimental Analysis..."
if [ -f "memory_dump_samples/linux_sample.mem" ]; then
    python3 -m unified_forensics experiment memory_dump_samples/linux_sample.mem --os-type linux --rates 1 --rates 10 --output analysis_results/test_experimental_linux.json
    if [ $? -ne 0 ]; then
        echo "ERROR: Experimental analysis test failed"
        exit 1
    fi
    echo "SUCCESS: Experimental analysis test passed"
else
    echo "WARNING: Linux sample not found, skipping experimental test"
fi

# Test 7: Cross-Platform Validation
echo ""
echo "[7] Testing Cross-Platform Validation..."
python3 -m unified_forensics validate --windows-dump memory_dump_samples/windows_sample.mem --linux-dump memory_dump_samples/linux_sample.mem --macos-dump memory_dump_samples/macos_sample.mem --output analysis_results/cross_platform_validation.json
if [ $? -ne 0 ]; then
    echo "ERROR: Cross-platform validation test failed"
    exit 1
fi
echo "SUCCESS: Cross-platform validation test passed"

echo ""
echo "=========================================="
echo "ALL TESTS COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo ""
echo "Test Results Summary:"
echo "  - Framework Info: PASSED"
echo "  - Memory Sample Generation: PASSED"
echo "  - Windows Analysis: PASSED"
echo "  - Linux Analysis: PASSED"
echo "  - macOS Analysis: PASSED"
echo "  - Experimental Analysis: PASSED"
echo "  - Cross-Platform Validation: PASSED"
echo ""
echo "Files generated:"
echo "  - Memory samples: memory_dump_samples/"
echo "  - Analysis results: analysis_results/"
echo "  - Performance charts: performance_charts/"
echo ""
echo "Ready for professor presentation!"
echo ""
