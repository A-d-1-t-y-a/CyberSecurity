import os
import struct
import random
import sys
from datetime import datetime

def create_memory_dump_sample(filename="sample_memory_dump.mem", size_mb=10, os_type="windows"):
    """
    Create a realistic memory dump sample for testing purposes
    
    Args:
        filename: Output filename for the memory dump
        size_mb: Size of the memory dump in megabytes
        os_type: Target operating system (windows, linux, macos)
    
    Returns:
        str: Path to the created memory dump file
    """
    print(f"Creating {os_type} memory dump sample: {filename} ({size_mb}MB)")
    
    test_data = bytearray()
    
    if os_type.lower() == "windows":
        test_data.extend(b'Windows NTOSKRNL Microsoft Corporation')
        test_data.extend(b'\x00' * 100)
        
        # Add Windows-specific structures with dynamic data
        process_count = random.randint(30, 80)
        for i in range(process_count):
            pid = random.randint(1000, 9999)
            process_names = ['explorer.exe', 'chrome.exe', 'notepad.exe', 'cmd.exe', 'svchost.exe']
            name = random.choice(process_names).encode('utf-8')
            test_data.extend(struct.pack('<I', pid))
            test_data.extend(name)
            test_data.extend(b'\x00' * (32 - len(name)))
        
        # Add Windows network structures with random data
        for i in range(random.randint(10, 30)):
            local_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            local_port = random.randint(1000, 65535)
            remote_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            remote_port = random.randint(1, 65535)
            network_str = f"{local_ip}:{local_port}->{remote_ip}:{remote_port}".encode('utf-8')
            test_data.extend(network_str)
            test_data.extend(b'\x00' * (64 - len(network_str)))
        
        # Add Windows kernel modules with random data
        module_count = random.randint(15, 25)
        module_names = ['ntoskrnl.exe', 'hal.dll', 'win32k.sys', 'ntdll.dll', 'kernel32.dll']
        for i in range(module_count):
            module_name = f"{random.choice(module_names)}_{i}".encode('utf-8')
            test_data.extend(module_name)
            test_data.extend(b'\x00' * (64 - len(module_name)))
    
    elif os_type.lower() == "linux":
        test_data.extend(b'Linux kernel vmlinux')
        test_data.extend(b'\x00' * 100)
        
        # Add Linux-specific structures with dynamic data
        process_count = random.randint(30, 80)
        for i in range(process_count):
            pid = random.randint(1000, 9999)
            process_names = ['init', 'systemd', 'bash', 'sshd', 'apache2', 'mysql']
            name = random.choice(process_names).encode('utf-8')
            test_data.extend(struct.pack('<I', pid))
            test_data.extend(name)
            test_data.extend(b'\x00' * (32 - len(name)))
        
        # Add Linux network structures with random data
        for i in range(random.randint(10, 30)):
            local_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            local_port = random.randint(1000, 65535)
            remote_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            remote_port = random.randint(1, 65535)
            network_str = f"{local_ip}:{local_port}->{remote_ip}:{remote_port}".encode('utf-8')
            test_data.extend(network_str)
            test_data.extend(b'\x00' * (64 - len(network_str)))
        
        # Add Linux kernel modules with random data
        module_count = random.randint(15, 25)
        module_names = ['ext4', 'nfs', 'tcp', 'udp', 'ipv6', 'bridge']
        for i in range(module_count):
            module_name = f"{random.choice(module_names)}_{i}.ko".encode('utf-8')
            test_data.extend(module_name)
            test_data.extend(b'\x00' * (64 - len(module_name)))
    
    elif os_type.lower() == "macos":
        test_data.extend(b'Darwin XNU mach_kernel')
        test_data.extend(b'\x00' * 100)
        
        # Add macOS-specific structures with dynamic data
        process_count = random.randint(30, 80)
        for i in range(process_count):
            pid = random.randint(1000, 9999)
            process_names = ['kernel_task', 'launchd', 'WindowServer', 'Dock', 'Finder', 'Safari']
            name = random.choice(process_names).encode('utf-8')
            test_data.extend(struct.pack('<I', pid))
            test_data.extend(name)
            test_data.extend(b'\x00' * (32 - len(name)))
        
        # Add macOS network structures with random data
        for i in range(random.randint(10, 30)):
            local_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            local_port = random.randint(1000, 65535)
            remote_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            remote_port = random.randint(1, 65535)
            network_str = f"{local_ip}:{local_port}->{remote_ip}:{remote_port}".encode('utf-8')
            test_data.extend(network_str)
            test_data.extend(b'\x00' * (64 - len(network_str)))
        
        # Add macOS kernel modules with random data
        module_count = random.randint(15, 25)
        module_names = ['IOKit', 'CoreFoundation', 'Security', 'SystemConfiguration', 'CFNetwork']
        for i in range(module_count):
            module_name = f"{random.choice(module_names)}_{i}.kext".encode('utf-8')
            test_data.extend(module_name)
            test_data.extend(b'\x00' * (64 - len(module_name)))
    
    # Fill remaining space
    target_size = size_mb * 1024 * 1024
    while len(test_data) < target_size:
        test_data.extend(b'\x00' * min(1024, target_size - len(test_data)))
    
    with open(filename, 'wb') as f:
        f.write(test_data)
    
    print(f"Test memory dump created: {filename}")
    print(f"Size: {os.path.getsize(filename) / (1024*1024):.2f} MB")
    return filename

def create_cross_platform_memory_samples():
    """
    Create memory dump samples for all supported operating systems
    
    Returns:
        dict: Dictionary mapping OS types to their respective memory dump file paths
    """
    import os
    os.makedirs('memory_dump_samples', exist_ok=True)
    
    memory_samples = {}
    
    # Create Windows memory sample
    windows_sample = create_memory_dump_sample("memory_dump_samples/windows_sample.mem", 50, "windows")
    memory_samples['windows'] = windows_sample
    
    # Create Linux memory sample
    linux_sample = create_memory_dump_sample("memory_dump_samples/linux_sample.mem", 50, "linux")
    memory_samples['linux'] = linux_sample
    
    # Create macOS memory sample
    macos_sample = create_memory_dump_sample("memory_dump_samples/macos_sample.mem", 50, "macos")
    memory_samples['macos'] = macos_sample
    
    return memory_samples

def main():
    """
    Main function for memory dump generator
    Usage:
        python memory_dump_generator.py all                    # Create samples for all platforms
        python memory_dump_generator.py <filename> <os> <size> # Create specific sample
        python memory_dump_generator.py                        # Create default Windows sample
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            # Create memory samples for all platforms
            memory_samples = create_cross_platform_memory_samples()
            print(f"\nCreated memory dump samples for all platforms:")
            for os_type, sample_path in memory_samples.items():
                print(f"  {os_type}: {sample_path}")
            print(f"\nYou can now test cross-platform validation with:")
            print(f"py -m unified_forensics validate --windows-dump {memory_samples['windows']} --linux-dump {memory_samples['linux']} --macos-dump {memory_samples['macos']}")
        else:
            filename = sys.argv[1]
            os_type = sys.argv[2] if len(sys.argv) > 2 else "windows"
            size_mb = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            
            create_memory_dump_sample(filename, size_mb, os_type)
            print(f"\nYou can now test the framework with:")
            print(f"py -m unified_forensics analyze {filename}")
            print(f"py -m unified_forensics experiment {filename} --os {os_type}")
    else:
        filename = "sample_memory_dump.mem"
        size_mb = 10
        os_type = "windows"
        
        create_memory_dump_sample(filename, size_mb, os_type)
        print(f"\nYou can now test the framework with:")
        print(f"py -m unified_forensics analyze {filename}")
        print(f"py -m unified_forensics experiment {filename} --os {os_type}")
        print(f"\nTo create memory samples for all platforms, run:")
        print(f"python memory_dump_generator.py all")

if __name__ == "__main__":
    main()
