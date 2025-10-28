#!/usr/bin/env python3
"""
Quick Memory Sample Generator for Testing
Creates small memory dump samples quickly for testing purposes
"""

import os
import struct
import random

def create_quick_sample(filename, os_type, size_mb=5):
    """Create a quick memory dump sample for testing"""
    print(f"Creating {os_type} sample: {filename} ({size_mb}MB)")
    
    test_data = bytearray()
    
    if os_type.lower() == "windows":
        test_data.extend(b'Windows NTOSKRNL Microsoft Corporation')
    elif os_type.lower() == "linux":
        test_data.extend(b'Linux kernel vmlinux')
    elif os_type.lower() == "macos":
        test_data.extend(b'Darwin XNU mach_kernel')
    
    # Add some basic structures
    test_data.extend(b'\x00' * 1000)
    
    # Fill to target size
    target_size = size_mb * 1024 * 1024
    while len(test_data) < target_size:
        test_data.extend(b'\x00' * min(1024, target_size - len(test_data)))
    
    with open(filename, 'wb') as f:
        f.write(test_data)
    
    print(f"Created: {filename} ({os.path.getsize(filename) / (1024*1024):.1f} MB)")
    return filename

def main():
    """Create quick samples for all platforms"""
    os.makedirs('memory_dump_samples', exist_ok=True)
    
    platforms = ['windows', 'linux', 'macos']
    for platform in platforms:
        filename = f"memory_dump_samples/{platform}_sample.mem"
        create_quick_sample(filename, platform, 5)  # 5MB samples for quick testing
    
    print("SUCCESS: All quick samples created!")

if __name__ == "__main__":
    main()
