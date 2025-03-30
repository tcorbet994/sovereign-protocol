import torch
import torch.nn as nn
from typing import Dict, Any, List, Optional
import numpy as np
from dataclasses import dataclass
import os
import json
from datetime import datetime

@dataclass
class TrainingStage:
    name: str
    description: str
    status: str
    progress: float
    metrics: Dict[str, float]

class CurriculumManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_stage = 0
        self.stages: List[TrainingStage] = []
        self.initialize_stages()
        
    def initialize_stages(self):
        """Initialize training stages"""
        self.stages = [
            TrainingStage(
                name="Human Knowledge Mastery",
                description="Comprehensive knowledge acquisition from diverse sources",
                status="pending",
                progress=0.0,
                metrics={}
            ),
            TrainingStage(
                name="Synthetic Reality Generation",
                description="Self-generated training data via synthetic realities",
                status="pending",
                progress=0.0,
                metrics={}
            ),
            TrainingStage(
                name="Quantum Self-Play",
                description="Advanced training through quantum computing",
                status="pending",
                progress=0.0,
                metrics={}
            )
        ]
    
    def update_stage_progress(self, stage_idx: int, metrics: Dict[str, float]):
        """Update progress and metrics for a training stage"""
        if 0 <= stage_idx < len(self.stages):
            self.stages[stage_idx].metrics.update(metrics)
            self.stages[stage_idx].progress = self._calculate_stage_progress(stage_idx)
            
            # Update stage status
            if self.stages[stage_idx].progress >= 1.0:
                self.stages[stage_idx].status = "completed"
            elif self.stages[stage_idx].progress > 0:
                self.stages[stage_idx].status = "in_progress"
    
    def _calculate_stage_progress(self, stage_idx: int) -> float:
        """Calculate progress for a specific stage"""
        stage = self.stages[stage_idx]
        
        if stage.name == "Human Knowledge Mastery":
            return self._calculate_knowledge_progress(stage.metrics)
        elif stage.name == "Synthetic Reality Generation":
            return self._calculate_synthetic_progress(stage.metrics)
        elif stage.name == "Quantum Self-Play":
            return self._calculate_quantum_progress(stage.metrics)
        
        return 0.0
    
    def _calculate_knowledge_progress(self, metrics: Dict[str, float]) -> float:
        """Calculate progress for human knowledge mastery stage"""
        required_metrics = {
            'knowledge_coverage': 0.8,
            'source_diversity': 0.7,
            'comprehension_score': 0.9
        }
        
        if not all(k in metrics for k in required_metrics):
            return 0.0
        
        # Weighted average of metrics
        weights = {'knowledge_coverage': 0.4, 'source_diversity': 0.3, 'comprehension_score': 0.3}
        progress = sum(metrics[k] * weights[k] for k in required_metrics)
        
        return min(1.0, progress)
    
    def _calculate_synthetic_progress(self, metrics: Dict[str, float]) -> float:
        """Calculate progress for synthetic reality generation stage"""
        required_metrics = {
            'reality_quality': 0.8,
            'diversity_score': 0.7,
            'coherence_score': 0.9
        }
        
        if not all(k in metrics for k in required_metrics):
            return 0.0
        
        # Weighted average of metrics
        weights = {'reality_quality': 0.4, 'diversity_score': 0.3, 'coherence_score': 0.3}
        progress = sum(metrics[k] * weights[k] for k in required_metrics)
        
        return min(1.0, progress)
    
    def _calculate_quantum_progress(self, metrics: Dict[str, float]) -> float:
        """Calculate progress for quantum self-play stage"""
        required_metrics = {
            'quantum_coherence': 0.8,
            'self_play_score': 0.7,
            'autonomy_level': 0.9
        }
        
        if not all(k in metrics for k in required_metrics):
            return 0.0
        
        # Weighted average of metrics
        weights = {'quantum_coherence': 0.4, 'self_play_score': 0.3, 'autonomy_level': 0.3}
        progress = sum(metrics[k] * weights[k] for k in required_metrics)
        
        return min(1.0, progress)
    
    def get_current_stage(self) -> TrainingStage:
        """Get current training stage"""
        return self.stages[self.current_stage]
    
    def advance_stage(self) -> bool:
        """Advance to next training stage if current is completed"""
        if self.current_stage < len(self.stages) - 1:
            current_stage = self.stages[self.current_stage]
            if current_stage.status == "completed":
                self.current_stage += 1
                return True
        return False
    
    def save_progress(self, path: str):
        """Save training progress"""
        progress_data = {
            'current_stage': self.current_stage,
            'stages': [
                {
                    'name': stage.name,
                    'status': stage.status,
                    'progress': stage.progress,
                    'metrics': stage.metrics
                }
                for stage in self.stages
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(progress_data, f, indent=2)
    
    def load_progress(self, path: str) -> bool:
        """Load training progress"""
        if not os.path.exists(path):
            return False
        
        try:
            with open(path, 'r') as f:
                progress_data = json.load(f)
            
            self.current_stage = progress_data['current_stage']
            
            for i, stage_data in enumerate(progress_data['stages']):
                if i < len(self.stages):
                    self.stages[i].status = stage_data['status']
                    self.stages[i].progress = stage_data['progress']
                    self.stages[i].metrics = stage_data['metrics']
            
            return True
        except:
            return False
    
    def get_training_metrics(self) -> Dict[str, Any]:
        """Get overall training metrics"""
        return {
            'current_stage': self.current_stage,
            'total_progress': sum(stage.progress for stage in self.stages) / len(self.stages),
            'stages': [
                {
                    'name': stage.name,
                    'status': stage.status,
                    'progress': stage.progress,
                    'metrics': stage.metrics
                }
                for stage in self.stages
            ]
        } 