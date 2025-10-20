import os
import json
import tempfile
from code.core import analyze_memory, detect_os_from_hint, choose_tool

def test_detect_os_from_hint_windows():
	assert detect_os_from_hint("windows_mem.mem") == "windows"

def test_detect_os_from_hint_linux():
	assert detect_os_from_hint("ubuntu_mem.mem") == "linux"

def test_choose_tool():
	assert choose_tool("windows") == "volatility"
	assert choose_tool("linux") == "rekall"
	assert choose_tool("macos") == "memprocfs"

def test_analyze_memory_stub():
	fd, path = tempfile.mkstemp(suffix=".mem")
	os.close(fd)
	try:
		res = analyze_memory(path)
		assert "metadata" in res
		assert "processes" in res
	finally:
		os.unlink(path)
