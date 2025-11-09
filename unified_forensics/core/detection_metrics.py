import json
import logging
import time
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import numpy as np

@dataclass
class DetectionMetrics:
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
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = DetectionMetrics()
        self.event_tracker = defaultdict(list)
        self.ground_truth_events = []
        self.detected_events = []
        self.start_time = None
        self.end_time = None
    
    def start_analysis(self):
        self.start_time = time.time()
        self.logger.info("Analysis timing started")
    
    def end_analysis(self):
        self.end_time = time.time()
        if self.start_time:
            self.metrics.analysis_time = self.end_time - self.start_time
            self.logger.info(f"Analysis completed in {self.metrics.analysis_time:.2f} seconds")
    
    def set_ground_truth(self, events: List[Dict[str, Any]]):
        self.ground_truth_events = events
        self.metrics.actual_events = len(events)
        self.logger.info(f"Ground truth set: {len(events)} events")
    
    def add_detected_event(self, event: Dict[str, Any], event_type: str = "unknown"):
        self.detected_events.append(event)
        self.event_tracker[event_type].append(event)
        self.metrics.returned_events = len(self.detected_events)
        self.logger.debug(f"Detected event added: {event_type}")
    
    def calculate_metrics(self) -> DetectionMetrics:
        if self.start_time and self.end_time:
            self.metrics.analysis_time = self.end_time - self.start_time
            self.metrics.events_per_second = self.metrics.actual_events / self.metrics.analysis_time if self.metrics.analysis_time > 0 else 0
        
        if self.metrics.actual_events > 0:
            self.metrics.detection_percentage = (self.metrics.returned_events / self.metrics.actual_events) * 100
        self._calculate_classification_metrics()
        self.logger.info(f"Detection metrics calculated: {self.metrics.detection_percentage:.2f}% detection rate")
        return self.metrics
    
    def _calculate_classification_metrics(self):
        matched_events = self._match_events()
        self.metrics.true_positives = len(matched_events)
        self.metrics.false_positives = self.metrics.returned_events - self.metrics.true_positives
        self.metrics.false_negatives = self.metrics.actual_events - self.metrics.true_positives
        
        if self.metrics.returned_events > 0:
            self.metrics.precision = self.metrics.true_positives / self.metrics.returned_events
        
        if self.metrics.actual_events > 0:
            self.metrics.recall = self.metrics.true_positives / self.metrics.actual_events
        
        if self.metrics.precision + self.metrics.recall > 0:
            self.metrics.f1_score = 2 * (self.metrics.precision * self.metrics.recall) / (self.metrics.precision + self.metrics.recall)
    
    def _match_events(self) -> List[Dict[str, Any]]:
        matched = []
        for detected in self.detected_events:
            for truth in self.ground_truth_events:
                if self._events_match(detected, truth):
                    matched.append(detected)
                    break
        return matched
    
    def _events_match(self, detected: Dict[str, Any], truth: Dict[str, Any]) -> bool:
        if 'name' in detected and 'name' in truth:
            return (detected.get('name') == truth.get('name') and 
                    detected.get('pid') == truth.get('pid'))
        
        if 'local_address' in detected and 'local_address' in truth:
            return (detected.get('local_address') == truth.get('local_address') and
                    detected.get('local_port') == truth.get('local_port') and
                    detected.get('remote_address') == truth.get('remote_address') and
                    detected.get('remote_port') == truth.get('remote_port'))
        
        if 'base_address' in detected and 'base_address' in truth:
            return (detected.get('name') == truth.get('name') and
                    detected.get('base_address') == truth.get('base_address'))
        
        return False
    
    def get_detailed_metrics(self) -> Dict[str, Any]:
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
            'by_event_type': {},
            'raw_data': {
                'ground_truth_events': self.ground_truth_events,
                'detected_events': self.detected_events
            }
        }
        
        for event_type, events in self.event_tracker.items():
            if events:
                detailed['by_event_type'][event_type] = {
                    'count': len(events),
                    'percentage': (len(events) / self.metrics.actual_events * 100) if self.metrics.actual_events > 0 else 0
                }
        
        return detailed
    
    def export_metrics(self, filename: str):
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
        self.metrics = DetectionMetrics()
        self.event_tracker = defaultdict(list)
        self.ground_truth_events = []
        self.detected_events = []
        self.start_time = None
        self.end_time = None
        self.logger.info("Metrics reset for new analysis")
