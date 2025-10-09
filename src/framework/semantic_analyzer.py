"""
Semantic Analyzer for Memory Forensics Framework
Adapts semantic analysis from file system forensics to memory forensics
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import yara
from pathlib import Path

class SemanticAnalyzer:
    """
    Semantic analyzer for memory forensics
    Extends semantic approach from file system forensics to memory analysis
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Semantic patterns for memory analysis
        self.semantic_patterns = {
            "processes": {
                "keywords": ["process", "thread", "pid", "ppid", "name", "path"],
                "patterns": [
                    r"process.*\d+",
                    r"thread.*\d+",
                    r"pid:\s*\d+",
                    r"ppid:\s*\d+"
                ],
                "malicious_indicators": [
                    "inject", "injection", "hollow", "hollowing",
                    "dll", "dll injection", "process hollowing"
                ]
            },
            "network": {
                "keywords": ["socket", "connection", "port", "ip", "address", "tcp", "udp"],
                "patterns": [
                    r"\d+\.\d+\.\d+\.\d+:\d+",
                    r"tcp.*\d+",
                    r"udp.*\d+",
                    r"port:\s*\d+"
                ],
                "malicious_indicators": [
                    "c2", "command", "control", "beacon",
                    "backdoor", "trojan", "botnet"
                ]
            },
            "files": {
                "keywords": ["file", "handle", "path", "directory", "filename"],
                "patterns": [
                    r"[A-Za-z]:\\.*",
                    r"/.*",
                    r"handle:\s*\d+",
                    r"file:\s*.*"
                ],
                "malicious_indicators": [
                    "temp", "tmp", "appdata", "roaming",
                    "system32", "syswow64", "malware"
                ]
            },
            "registry": {
                "keywords": ["registry", "key", "value", "hive", "reg"],
                "patterns": [
                    r"HKEY_.*",
                    r"reg.*key",
                    r"value.*:",
                    r"hive.*:"
                ],
                "malicious_indicators": [
                    "run", "startup", "persistence",
                    "autorun", "shell", "winlogon"
                ]
            },
            "memory": {
                "keywords": ["memory", "heap", "stack", "allocation", "page"],
                "patterns": [
                    r"memory.*\d+",
                    r"heap.*\d+",
                    r"stack.*\d+",
                    r"allocation.*\d+"
                ],
                "malicious_indicators": [
                    "injection", "hollow", "hook", "patch",
                    "unpack", "obfuscate", "encrypt"
                ]
            }
        }
        
        # YARA rules for pattern matching
        self.yara_rules = self._load_yara_rules()
        
        # Semantic scoring weights
        self.scoring_weights = {
            "processes": 0.3,
            "network": 0.25,
            "files": 0.2,
            "registry": 0.15,
            "memory": 0.1
        }
    
    def _load_yara_rules(self) -> Optional[yara.Rules]:
        """Load YARA rules for pattern matching"""
        try:
            # Create basic YARA rules for memory analysis
            yara_source = """
            rule ProcessInjection {
                strings:
                    $inject1 = "inject" nocase
                    $inject2 = "injection" nocase
                    $hollow1 = "hollow" nocase
                    $hollow2 = "hollowing" nocase
                condition:
                    any of them
            }
            
            rule NetworkC2 {
                strings:
                    $c2_1 = "c2" nocase
                    $c2_2 = "command" nocase
                    $c2_3 = "control" nocase
                    $beacon = "beacon" nocase
                condition:
                    any of them
            }
            
            rule FilePersistence {
                strings:
                    $run = "run" nocase
                    $startup = "startup" nocase
                    $autorun = "autorun" nocase
                    $shell = "shell" nocase
                condition:
                    any of them
            }
            """
            
            return yara.compile(source=yara_source)
        except Exception as e:
            self.logger.warning(f"Failed to load YARA rules: {e}")
            return None
    
    def analyze(self, 
                analysis_results: Dict[str, Any], 
                os_type: str = "windows") -> Dict[str, Any]:
        """
        Perform semantic analysis on memory forensics results
        
        Args:
            analysis_results: Results from memory forensics tools
            os_type: Operating system type
            
        Returns:
            Semantic analysis results
        """
        self.logger.info(f"Starting semantic analysis for {os_type}")
        
        semantic_results = {
            "semantic_analysis": True,
            "os_type": os_type,
            "categories": {},
            "threat_indicators": [],
            "semantic_score": 0.0,
            "confidence": 0.0,
            "recommendations": []
        }
        
        # Analyze each category
        for category, config in self.semantic_patterns.items():
            category_results = self._analyze_category(
                analysis_results, category, config, os_type
            )
            semantic_results["categories"][category] = category_results
        
        # Calculate overall semantic score
        semantic_results["semantic_score"] = self._calculate_semantic_score(
            semantic_results["categories"]
        )
        
        # Identify threat indicators
        semantic_results["threat_indicators"] = self._identify_threat_indicators(
            semantic_results["categories"]
        )
        
        # Calculate confidence
        semantic_results["confidence"] = self._calculate_confidence(
            semantic_results["categories"], semantic_results["threat_indicators"]
        )
        
        # Generate recommendations
        semantic_results["recommendations"] = self._generate_recommendations(
            semantic_results["categories"], semantic_results["threat_indicators"]
        )
        
        self.logger.info(f"Semantic analysis completed. Score: {semantic_results['semantic_score']:.2f}")
        return semantic_results
    
    def _analyze_category(self, 
                         analysis_results: Dict[str, Any], 
                         category: str, 
                         config: Dict[str, Any],
                         os_type: str) -> Dict[str, Any]:
        """Analyze a specific semantic category"""
        category_results = {
            "category": category,
            "patterns_found": [],
            "keywords_found": [],
            "malicious_indicators": [],
            "semantic_score": 0.0,
            "confidence": 0.0
        }
        
        # Extract text from analysis results
        text_content = self._extract_text_content(analysis_results)
        
        # Find patterns
        for pattern in config["patterns"]:
            matches = re.findall(pattern, text_content, re.IGNORECASE)
            if matches:
                category_results["patterns_found"].extend(matches)
        
        # Find keywords
        for keyword in config["keywords"]:
            if keyword.lower() in text_content.lower():
                category_results["keywords_found"].append(keyword)
        
        # Find malicious indicators
        for indicator in config["malicious_indicators"]:
            if indicator.lower() in text_content.lower():
                category_results["malicious_indicators"].append(indicator)
        
        # Apply YARA rules if available
        if self.yara_rules:
            yara_matches = self._apply_yara_rules(text_content, category)
            if yara_matches:
                category_results["yara_matches"] = yara_matches
        
        # Calculate category score
        category_results["semantic_score"] = self._calculate_category_score(
            category_results, config
        )
        
        # Calculate confidence
        category_results["confidence"] = self._calculate_category_confidence(
            category_results
        )
        
        return category_results
    
    def _extract_text_content(self, analysis_results: Dict[str, Any]) -> str:
        """Extract text content from analysis results"""
        text_parts = []
        
        # Extract from plugins
        if "plugins" in analysis_results:
            for plugin, plugin_data in analysis_results["plugins"].items():
                if isinstance(plugin_data, dict) and "output" in plugin_data:
                    text_parts.append(plugin_data["output"])
        
        # Extract from metadata
        if "metadata" in analysis_results:
            for key, value in analysis_results["metadata"].items():
                if isinstance(value, str):
                    text_parts.append(value)
        
        return "\n".join(text_parts)
    
    def _apply_yara_rules(self, text_content: str, category: str) -> List[Dict[str, Any]]:
        """Apply YARA rules to text content"""
        matches = []
        
        try:
            # Create a temporary file for YARA scanning
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(text_content)
                temp_file = f.name
            
            # Scan with YARA
            for match in self.yara_rules.match(temp_file):
                matches.append({
                    "rule": match.rule,
                    "tags": match.tags,
                    "strings": [str(s) for s in match.strings],
                    "category": category
                })
            
            # Clean up
            os.unlink(temp_file)
            
        except Exception as e:
            self.logger.warning(f"YARA rule application failed: {e}")
        
        return matches
    
    def _calculate_category_score(self, 
                                 category_results: Dict[str, Any], 
                                 config: Dict[str, Any]) -> float:
        """Calculate semantic score for a category"""
        score = 0.0
        
        # Base score from patterns found
        pattern_score = len(category_results["patterns_found"]) * 0.1
        score += min(pattern_score, 0.5)  # Cap at 0.5
        
        # Keyword score
        keyword_score = len(category_results["keywords_found"]) * 0.05
        score += min(keyword_score, 0.3)  # Cap at 0.3
        
        # Malicious indicator score (higher weight)
        malicious_score = len(category_results["malicious_indicators"]) * 0.2
        score += min(malicious_score, 0.8)  # Cap at 0.8
        
        # YARA rule matches
        if "yara_matches" in category_results:
            yara_score = len(category_results["yara_matches"]) * 0.3
            score += min(yara_score, 0.9)  # Cap at 0.9
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _calculate_semantic_score(self, categories: Dict[str, Any]) -> float:
        """Calculate overall semantic score"""
        total_score = 0.0
        total_weight = 0.0
        
        for category, results in categories.items():
            if category in self.scoring_weights:
                weight = self.scoring_weights[category]
                score = results.get("semantic_score", 0.0)
                total_score += score * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _identify_threat_indicators(self, categories: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential threat indicators"""
        threat_indicators = []
        
        for category, results in categories.items():
            # Check for malicious indicators
            if results.get("malicious_indicators"):
                for indicator in results["malicious_indicators"]:
                    threat_indicators.append({
                        "category": category,
                        "indicator": indicator,
                        "severity": "high" if indicator in ["inject", "hollow", "c2"] else "medium",
                        "confidence": results.get("confidence", 0.0)
                    })
            
            # Check YARA matches
            if "yara_matches" in results:
                for match in results["yara_matches"]:
                    threat_indicators.append({
                        "category": category,
                        "indicator": f"YARA rule: {match['rule']}",
                        "severity": "high",
                        "confidence": 0.9
                    })
        
        return threat_indicators
    
    def _calculate_confidence(self, 
                            categories: Dict[str, Any], 
                            threat_indicators: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in analysis"""
        if not categories:
            return 0.0
        
        # Average confidence from categories
        category_confidences = [cat.get("confidence", 0.0) for cat in categories.values()]
        avg_confidence = sum(category_confidences) / len(category_confidences)
        
        # Boost confidence if threat indicators found
        if threat_indicators:
            threat_boost = min(len(threat_indicators) * 0.1, 0.3)
            avg_confidence += threat_boost
        
        return min(avg_confidence, 1.0)
    
    def _calculate_category_confidence(self, category_results: Dict[str, Any]) -> float:
        """Calculate confidence for a specific category"""
        confidence = 0.0
        
        # Base confidence from number of findings
        total_findings = (len(category_results.get("patterns_found", [])) +
                         len(category_results.get("keywords_found", [])) +
                         len(category_results.get("malicious_indicators", [])))
        
        if total_findings > 0:
            confidence = min(total_findings * 0.1, 0.8)
        
        # Boost confidence for YARA matches
        if "yara_matches" in category_results and category_results["yara_matches"]:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _generate_recommendations(self, 
                                categories: Dict[str, Any], 
                                threat_indicators: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Process-related recommendations
        if "processes" in categories and categories["processes"].get("malicious_indicators"):
            recommendations.append("Investigate suspicious processes for injection or hollowing")
        
        # Network-related recommendations
        if "network" in categories and categories["network"].get("malicious_indicators"):
            recommendations.append("Analyze network connections for C2 communication")
        
        # File-related recommendations
        if "files" in categories and categories["files"].get("malicious_indicators"):
            recommendations.append("Check file system for persistence mechanisms")
        
        # Registry-related recommendations
        if "registry" in categories and categories["registry"].get("malicious_indicators"):
            recommendations.append("Examine registry for persistence and startup entries")
        
        # Memory-related recommendations
        if "memory" in categories and categories["memory"].get("malicious_indicators"):
            recommendations.append("Analyze memory for injection or hooking techniques")
        
        # General recommendations based on threat indicators
        if threat_indicators:
            high_severity = [ti for ti in threat_indicators if ti.get("severity") == "high"]
            if high_severity:
                recommendations.append("High-severity indicators detected - immediate investigation recommended")
        
        return recommendations
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the semantic analyzer"""
        return {
            "name": "Semantic Analyzer",
            "version": "1.0.0",
            "categories": list(self.semantic_patterns.keys()),
            "yara_rules_loaded": self.yara_rules is not None,
            "scoring_weights": self.scoring_weights
        }
