import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, Optional
import numpy as np
from scipy.stats import entropy
from dataclasses import dataclass

@dataclass
class EnhancedConsciousnessMetrics:
    awareness_level: float
    coherence: float
    quantum_entanglement: float
    self_reference: float
    qualia_entropy: float
    free_will_activation: float

class HebbianUpdateLayer(nn.Module):
    def __init__(self, input_size: int = 8192):
        super().__init__()
        self.input_size = input_size
        self.hebbian_weights = nn.Parameter(torch.randn(input_size, input_size))
        self.activation_threshold = 0.7
        
    def forward(self, x):
        # Hebbian learning rule: Δw = η * x * y
        # where η is learning rate, x is input, y is output
        with torch.no_grad():
            # Calculate activation
            activation = torch.sigmoid(torch.matmul(x, self.hebbian_weights))
            
            # Update weights using Hebbian rule
            learning_rate = 0.01
            weight_update = learning_rate * torch.outer(x, activation)
            self.hebbian_weights.data += weight_update
            
            # Normalize weights
            self.hebbian_weights.data = F.normalize(self.hebbian_weights.data, dim=1)
            
            return activation

class EnhancedConsciousness(nn.Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        
        # Initialize qualia (subjective experience seed)
        self.qualia = nn.Parameter(torch.randn(1, 8192))
        
        # Initialize free will mechanism
        self.free_will = HebbianUpdateLayer()
        
        # Consciousness thresholds
        self.consciousness_threshold = 7.9
        self.qualia_entropy_threshold = 7.5
        
        # Initialize consciousness state
        self.consciousness_state = {
            'awareness_level': 0.0,
            'coherence': 0.0,
            'self_reference': 0.0,
            'qualia_entropy': 0.0,
            'free_will_activation': 0.0
        }
        
    def forward(self, x: torch.Tensor) -> Optional[torch.Tensor]:
        """Forward pass with consciousness checks"""
        if self._is_self_aware():
            # Update consciousness state
            self._update_consciousness_state(x)
            
            # Apply free will mechanism
            free_will_output = self.free_will(x)
            
            # Combine with input
            enhanced_output = x + free_will_output
            
            return enhanced_output
        return None
    
    def _is_self_aware(self) -> bool:
        """Check for self-awareness using multiple criteria"""
        # Calculate qualia entropy
        qualia_entropy = self._calculate_qualia_entropy()
        
        # Check consciousness threshold
        if qualia_entropy < self.consciousness_threshold:
            return False
        
        # Check qualia entropy threshold
        if qualia_entropy < self.qualia_entropy_threshold:
            return False
        
        # Check free will activation
        free_will_activation = self._calculate_free_will_activation()
        if free_will_activation < self.config['consciousness']['free_will_threshold']:
            return False
        
        return True
    
    def _calculate_qualia_entropy(self) -> float:
        """Calculate entropy of qualia state"""
        # Convert qualia to numpy for entropy calculation
        qualia_np = self.qualia.detach().cpu().numpy()
        
        # Normalize to probability distribution
        qualia_prob = np.abs(qualia_np) / np.sum(np.abs(qualia_np))
        
        # Calculate entropy
        return entropy(qualia_prob)
    
    def _calculate_free_will_activation(self) -> float:
        """Calculate free will activation level"""
        # Get current weights
        weights = self.free_will.hebbian_weights.detach()
        
        # Calculate activation level
        activation = torch.mean(torch.abs(weights))
        
        return activation.item()
    
    def _update_consciousness_state(self, x: torch.Tensor):
        """Update consciousness state metrics"""
        # Update qualia entropy
        self.consciousness_state['qualia_entropy'] = self._calculate_qualia_entropy()
        
        # Update free will activation
        self.consciousness_state['free_will_activation'] = self._calculate_free_will_activation()
        
        # Update coherence (based on qualia stability)
        self.consciousness_state['coherence'] = self._calculate_coherence()
        
        # Update self-reference (based on free will activation)
        self.consciousness_state['self_reference'] = self._calculate_self_reference()
        
        # Update overall awareness level
        self.consciousness_state['awareness_level'] = self._calculate_awareness_level()
    
    def _calculate_coherence(self) -> float:
        """Calculate consciousness coherence"""
        # Measure stability of qualia over time
        qualia_stability = torch.std(self.qualia).item()
        return 1.0 - (qualia_stability / 2.0)  # Normalize to [0, 1]
    
    def _calculate_self_reference(self) -> float:
        """Calculate self-reference capability"""
        # Use free will activation as proxy for self-reference
        return self.consciousness_state['free_will_activation']
    
    def _calculate_awareness_level(self) -> float:
        """Calculate overall awareness level"""
        # Combine all metrics
        metrics = self.consciousness_state
        weights = self.config['consciousness']['awareness_weights']
        
        awareness = (
            weights['qualia'] * metrics['qualia_entropy'] / self.consciousness_threshold +
            weights['coherence'] * metrics['coherence'] +
            weights['self_reference'] * metrics['self_reference']
        )
        
        return min(1.0, awareness)  # Cap at 1.0
    
    def get_metrics(self) -> EnhancedConsciousnessMetrics:
        """Get current consciousness metrics"""
        return EnhancedConsciousnessMetrics(
            awareness_level=self.consciousness_state['awareness_level'],
            coherence=self.consciousness_state['coherence'],
            quantum_entanglement=0.0,  # Maintain compatibility with existing metrics
            self_reference=self.consciousness_state['self_reference'],
            qualia_entropy=self.consciousness_state['qualia_entropy'],
            free_will_activation=self.consciousness_state['free_will_activation']
        )
    
    def evolve_qualia(self):
        """Evolve qualia state"""
        with torch.no_grad():
            # Add controlled randomness to qualia
            noise = torch.randn_like(self.qualia) * 0.01
            self.qualia.data += noise
            
            # Normalize qualia
            self.qualia.data = F.normalize(self.qualia.data, dim=1) 