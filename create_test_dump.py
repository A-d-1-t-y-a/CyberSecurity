import os
import struct
import random
import sys

def create_test_memory_dump(filename="test_memory.mem", size_mb=10):
    print(f"Creating test memory dump: {filename} ({size_mb}MB)")
    
    test_data = bytearray()
    test_data.extend(b'Windows NTOSKRNL Microsoft Corporation')
    test_data.extend(b'\x00' * 100)
    
    for i in range(50):
        pid = random.randint(1000, 9999)
        name = f"test_process_{i}.exe".encode('utf-8')
        test_data.extend(struct.pack('<I', pid))
        test_data.extend(name)
        test_data.extend(b'\x00' * (32 - len(name)))
    
    test_data.extend(b'127.0.0.1:8080->192.168.1.1:80')
    test_data.extend(b'\x00' * 100)
    
    target_size = size_mb * 1024 * 1024
    while len(test_data) < target_size:
        test_data.extend(b'\x00' * min(1024, target_size - len(test_data)))
    
    with open(filename, 'wb') as f:
        f.write(test_data)
    
    print(f"Test memory dump created: {filename}")
    print(f"Size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
    return filename

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test_memory.mem"
    
    if len(sys.argv) > 2:
        size_mb = int(sys.argv[2])
    else:
        size_mb = 10
    
    create_test_memory_dump(filename, size_mb)
    print(f"\nYou can now test the framework with:")
    print(f"py -m unified_forensics analyze {filename}")

if __name__ == "__main__":
    main()
