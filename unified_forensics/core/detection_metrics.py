import json
import logging
import time
import threading
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import numpy as np

@dataclass
class DetectionMetrics:
    """Detection metrics for forensic analysis similar to paper section 6.2"""
    actual_events: int = 0
    returned_events: int = 0
    detection_percentage: float = 0.0
    false_positives: int = 0
    false_negatives: int = 0
    true_positives: int = 0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    analysis_time: float = 0.0
    events_per_second: float = 0.0

class DetectionMetricsCalculator:
    """Calculate detection metrics for memory forensics analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = DetectionMetrics()
        self.event_tracker = defaultdict(list)
        self.ground_truth_events = []
        self.detected_events = []
        self.start_time = None
        self.end_time = None
    
    def start_analysis(self):
        """Start timing the analysis"""
        self.start_time = time.time()
        self.logger.info("Analysis timing started")
    
    def end_analysis(self):
        """End timing the analysis"""
        self.end_time = time.time()
        if self.start_time:
            self.metrics.analysis_time = self.end_time - self.start_time
            self.logger.info(f"Analysis completed in {self.metrics.analysis_time:.2f} seconds")
    
    def set_ground_truth(self, events: List[Dict[str, Any]]):
        """Set ground truth events for comparison"""
        self.ground_truth_events = events
        self.metrics.actual_events = len(events)
        self.logger.info(f"Ground truth set: {len(events)} events")
    
    def add_detected_event(self, event: Dict[str, Any], event_type: str = "unknown"):
        """Add a detected event for metrics calculation"""
        self.detected_events.append(event)
        self.event_tracker[event_type].append(event)
        self.metrics.returned_events = len(self.detected_events)
        self.logger.debug(f"Detected event added: {event_type}")
    
    def calculate_metrics(self) -> DetectionMetrics:
        """Calculate comprehensive detection metrics"""
        if self.start_time and self.end_time:
            self.metrics.analysis_time = self.end_time - self.start_time
            self.metrics.events_per_second = self.metrics.actual_events / self.metrics.analysis_time if self.metrics.analysis_time > 0 else 0
        
        # Calculate detection percentage (as in paper)
        if self.metrics.actual_events > 0:
            self.metrics.detection_percentage = (self.metrics.returned_events / self.metrics.actual_events) * 100
        
        # Calculate precision, recall, F1-score
        self._calculate_classification_metrics()
        
        self.logger.info(f"Detection metrics calculated: {self.metrics.detection_percentage:.2f}% detection rate")
        return self.metrics
    
    def _calculate_classification_metrics(self):
        """Calculate precision, recall, and F1-score"""
        # Match detected events with ground truth
        matched_events = self._match_events()
        
        self.metrics.true_positives = len(matched_events)
        self.metrics.false_positives = self.metrics.returned_events - self.metrics.true_positives
        self.metrics.false_negatives = self.metrics.actual_events - self.metrics.true_positives
        
        # Calculate precision
        if self.metrics.returned_events > 0:
            self.metrics.precision = self.metrics.true_positives / self.metrics.returned_events
        
        # Calculate recall
        if self.metrics.actual_events > 0:
            self.metrics.recall = self.metrics.true_positives / self.metrics.actual_events
        
        # Calculate F1-score
        if self.metrics.precision + self.metrics.recall > 0:
            self.metrics.f1_score = 2 * (self.metrics.precision * self.metrics.recall) / (self.metrics.precision + self.metrics.recall)
    
    def _match_events(self) -> List[Dict[str, Any]]:
        """Match detected events with ground truth events"""
        matched = []
        
        for detected in self.detected_events:
            for truth in self.ground_truth_events:
                if self._events_match(detected, truth):
                    matched.append(detected)
                    break
        
        return matched
    
    def _events_match(self, detected: Dict[str, Any], truth: Dict[str, Any]) -> bool:
        """Check if two events match based on key attributes"""
        # Match on process name and PID for processes
        if 'name' in detected and 'name' in truth:
            return (detected.get('name') == truth.get('name') and 
                    detected.get('pid') == truth.get('pid'))
        
        # Match on network connections
        if 'local_address' in detected and 'local_address' in truth:
            return (detected.get('local_address') == truth.get('local_address') and
                    detected.get('local_port') == truth.get('local_port') and
                    detected.get('remote_address') == truth.get('remote_address') and
                    detected.get('remote_port') == truth.get('remote_port'))
        
        # Match on modules
        if 'base_address' in detected and 'base_address' in truth:
            return (detected.get('name') == truth.get('name') and
                    detected.get('base_address') == truth.get('base_address'))
        
        return False
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed metrics breakdown by event type"""
        detailed = {
            'overall': {
                'actual_events': self.metrics.actual_events,
                'returned_events': self.metrics.returned_events,
                'detection_percentage': self.metrics.detection_percentage,
                'analysis_time': self.metrics.analysis_time,
                'events_per_second': self.metrics.events_per_second
            },
            'classification': {
                'true_positives': self.metrics.true_positives,
                'false_positives': self.metrics.false_positives,
                'false_negatives': self.metrics.false_negatives,
                'precision': self.metrics.precision,
                'recall': self.metrics.recall,
                'f1_score': self.metrics.f1_score
            },
            'by_event_type': {}
        }
        
        # Calculate metrics by event type
        for event_type, events in self.event_tracker.items():
            if events:
                detailed['by_event_type'][event_type] = {
                    'count': len(events),
                    'percentage': (len(events) / self.metrics.actual_events * 100) if self.metrics.actual_events > 0 else 0
                }
        
        return detailed
    
    def export_metrics(self, filename: str):
        """Export metrics to JSON file"""
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.get_detailed_metrics(),
            'raw_data': {
                'ground_truth_events': self.ground_truth_events,
                'detected_events': self.detected_events
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        self.logger.info(f"Metrics exported to {filename}")
    
    def reset(self):
        """Reset all metrics for new analysis"""
        self.metrics = DetectionMetrics()
        self.event_tracker = defaultdict(list)
        self.ground_truth_events = []
        self.detected_events = []
        self.start_time = None
        self.end_time = None
        self.logger.info("Metrics reset for new analysis")

class EventGenerator:
    """Generate test events for metrics validation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_test_events(self, count: int, event_types: List[str] = None) -> List[Dict[str, Any]]:
        """Generate test events for validation"""
        if event_types is None:
            event_types = ['process', 'network', 'module', 'memory_region']
        
        events = []
        
        # Distribute events across types based on realistic ratios
        type_distribution = {
            'process': 0.4,      # 40% processes
            'network': 0.3,      # 30% network connections
            'module': 0.2,       # 20% modules
            'memory_region': 0.1  # 10% memory regions
        }
        
        for i in range(count):
            # Select event type based on distribution
            rand = np.random.random()
            cumulative = 0
            selected_type = event_types[0]  # default
            
            for event_type in event_types:
                cumulative += type_distribution.get(event_type, 0.25)
                if rand <= cumulative:
                    selected_type = event_type
                    break
            
            event = self._generate_event(selected_type, i)
            events.append(event)
        
        self.logger.info(f"Generated {count} test events")
        return events
    
    def _generate_event(self, event_type: str, index: int) -> Dict[str, Any]:
        """Generate a specific type of event"""
        base_time = datetime.now()
        
        if event_type == 'process':
            process_names = ['explorer.exe', 'chrome.exe', 'notepad.exe', 'cmd.exe', 'powershell.exe']
            return {
                'type': 'process',
                'pid': 1000 + index + np.random.randint(0, 100),
                'name': np.random.choice(process_names),
                'parent_pid': 1000 + (index // 10) + np.random.randint(0, 50),
                'command_line': f'{np.random.choice(process_names)} --arg{np.random.randint(1, 10)}',
                'start_time': datetime.fromtimestamp(base_time.timestamp() + np.random.randint(0, 3600)).isoformat()
            }
        elif event_type == 'network':
            protocols = ['tcp', 'udp']
            states = ['ESTABLISHED', 'LISTENING', 'CLOSE_WAIT', 'TIME_WAIT']
            return {
                'type': 'network',
                'local_address': f'192.168.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}',
                'local_port': 8000 + index + np.random.randint(0, 1000),
                'remote_address': f'{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}.{np.random.randint(1, 255)}',
                'remote_port': 80 + (index % 1000) + np.random.randint(0, 100),
                'protocol': np.random.choice(protocols),
                'state': np.random.choice(states)
            }
        elif event_type == 'module':
            module_names = ['ntdll.dll', 'kernel32.dll', 'user32.dll', 'advapi32.dll', 'ole32.dll']
            return {
                'type': 'module',
                'name': np.random.choice(module_names),
                'base_address': f'0x{np.random.randint(0x1000000, 0x7FFFFFFF):08x}',
                'size': 4096 + (index * 100) + np.random.randint(0, 10000),
                'path': f'C:\\Windows\\System32\\{np.random.choice(module_names)}'
            }
        elif event_type == 'memory_region':
            protections = ['PAGE_EXECUTE_READ', 'PAGE_READWRITE', 'PAGE_EXECUTE_READWRITE', 'PAGE_READONLY']
            region_types = ['MEM_PRIVATE', 'MEM_MAPPED', 'MEM_IMAGE']
            start_addr = np.random.randint(0x1000000, 0x7FFFFFFF)
            return {
                'type': 'memory_region',
                'start_address': f'0x{start_addr:08x}',
                'end_address': f'0x{start_addr + 4096 + np.random.randint(0, 100000):08x}',
                'size': 4096 + np.random.randint(0, 100000),
                'protection': np.random.choice(protections),
                'type': np.random.choice(region_types)
            }
        else:
            return {
                'type': 'unknown',
                'id': index,
                'data': f'test_data_{index}_{np.random.randint(1000, 9999)}'
            }
