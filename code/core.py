import os
import time
import json
from typing import Dict, Any, List
from jsonschema import validate

OUTPUT_SCHEMA = {	"type":"object",	"properties":{
		"metadata":{"type":"object"},
		"processes":{"type":"array"},
		"network_connections":{"type":"array"},
		"malware_indicators":{"type":"array"},
		"summary":{"type":"object"}
	},
	"required":["metadata","processes","network_connections","malware_indicators","summary"]
}

SUPPORTED_OS = ["windows","linux","macos"]

def detect_os_from_hint(path: str) -> str:
	name = os.path.basename(path).lower()
	if "win" in name:
		return "windows"
	if "lin" in name or "ubuntu" in name:
		return "linux"
	if "mac" in name or "osx" in name or "darwin" in name:
		return "macos"
	return "unknown"

def choose_tool(os_type: str) -> str:
	if os_type == "windows":
		return "volatility"
	if os_type == "linux":
		return "rekall"
	if os_type == "macos":
		return "memprocfs"
	return "volatility"

def stub_results() -> Dict[str, Any]:
	return {
		"metadata":{},
		"processes":[],
		"network_connections":[],
		"malware_indicators":[],
		"summary":{"total_processes":0,"suspicious_processes":0,"network_connections":0,"threat_level":"UNKNOWN"}
	}

def analyze_memory(dump_path: str, analysis_type: str = "full", verbose: bool = False) -> Dict[str, Any]:
	if not os.path.isfile(dump_path):
		raise FileNotFoundError(dump_path)
	start = time.time()
	os_type = detect_os_from_hint(dump_path)
	tool = choose_tool(os_type)
	data = run_tool(dump_path, tool, analysis_type)
	data["metadata"] = {
		"dump_file": dump_path,
		"os_detected": os_type,
		"tool_used": tool,
		"analysis_type": analysis_type,
		"duration_sec": round(time.time()-start,3)
	}
	validate(instance=data, schema=OUTPUT_SCHEMA)
	return data

def run_tool(dump_path: str, tool: str, analysis_type: str) -> Dict[str, Any]:
	results = stub_results()
	if tool == "volatility":
		from .tools.volatility_wrapper import run
		parsed = run(dump_path, analysis_type)
	elif tool == "rekall":
		from .tools.rekall_wrapper import run
		parsed = run(dump_path, analysis_type)
	else:
		from .tools.memprocfs_wrapper import run
		parsed = run(dump_path, analysis_type)
	results.update(parsed)
	return results
