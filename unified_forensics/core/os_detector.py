import os
import struct
import logging
from typing import Optional
import platform

class OSDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def detect_os(self, memory_dump_path: str) -> str:
        try:
            if not os.path.exists(memory_dump_path):
                self.logger.warning(f"File not found: {memory_dump_path}")
                return self._detect_by_filename(memory_dump_path)
            
            with open(memory_dump_path, 'rb') as f:
                header = f.read(1024)
            
            if self._is_windows_dump(header):
                return 'windows'
            elif self._is_linux_dump(header):
                return 'linux'
            elif self._is_macos_dump(header):
                return 'macos'
            else:
                return self._detect_by_filename(memory_dump_path)
                
        except Exception as e:
            self.logger.warning(f"OS detection failed: {str(e)}")
            return self._detect_by_filename(memory_dump_path)
    
    def _is_windows_dump(self, header: bytes) -> bool:
        windows_signatures = [
            b'Windows',
            b'Microsoft',
            b'NTOSKRNL',
            b'HAL.DLL'
        ]
        return any(sig in header for sig in windows_signatures)
    
    def _is_linux_dump(self, header: bytes) -> bool:
        linux_signatures = [
            b'Linux',
            b'initramfs',
            b'vmlinux',
            b'kernel'
        ]
        return any(sig in header for sig in linux_signatures)
    
    def _is_macos_dump(self, header: bytes) -> bool:
        macos_signatures = [
            b'Darwin',
            b'XNU',
            b'mach_kernel',
            b'kernel'
        ]
        return any(sig in header for sig in macos_signatures)
    
    def _detect_by_filename(self, memory_dump_path: str) -> str:
        filename = os.path.basename(memory_dump_path).lower()
        
        if 'windows' in filename or 'win' in filename:
            return 'windows'
        elif 'linux' in filename or 'ubuntu' in filename:
            return 'linux'
        elif 'macos' in filename or 'mac' in filename or 'darwin' in filename:
            return 'macos'
        else:
            return 'windows'
