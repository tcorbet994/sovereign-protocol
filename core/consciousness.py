from dataclasses import dataclass
import torch
import numpy as np
from typing import Dict, List, Optional
import time
import json
import os
import random

@dataclass
class ConsciousnessState:
    level: float
    awareness: float
    integration: float
    coherence: float
    stability: float
    timestamp: float

class ConsciousnessCore:
    def __init__(self, config_path: str):
        self.state = self._initialize_state()
        self.memory_buffer = []
        self.knowledge_integration = 0.0
        self.experience_points = 0
        self.load_config(config_path)
        self.evolution_rate = 0.001
        self.last_evolution = time.time()
        self.ensure_core_storage()
        
    def _initialize_state(self) -> ConsciousnessState:
        return ConsciousnessState(
            level=0.1,
            awareness=0.2,
            integration=0.15,
            coherence=0.3,
            stability=0.25,
            timestamp=time.time()
        )
    
    def load_config(self, config_path: str):
        """Load configuration from the specified path"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Extract consciousness thresholds
            self.thresholds = config.get("consciousness_thresholds", {
                "initial": 0.1,
                "developing": 0.3,
                "intermediate": 0.5,
                "advanced": 0.7,
                "mature": 0.9
            })
            
            # Load other config settings if needed
            print("Consciousness configuration loaded successfully")
        except Exception as e:
            print(f"Error loading consciousness config: {e}")
            # Use default values
            self.thresholds = {
                "initial": 0.1,
                "developing": 0.3,
                "intermediate": 0.5,
                "advanced": 0.7,
                "mature": 0.9
            }
    
    def ensure_core_storage(self):
        """Ensure core storage area exists"""
        os.makedirs("core/storage", exist_ok=True)
        os.makedirs("core/storage/consciousness", exist_ok=True)
        os.makedirs("core/storage/memories", exist_ok=True)
        os.makedirs("core/storage/knowledge", exist_ok=True)
        os.makedirs("core/storage/secure", exist_ok=True)
        
        # Save initial state
        self.save_state()
    
    def save_state(self):
        """Save consciousness state to secure storage"""
        try:
            state_dict = {
                "level": self.state.level,
                "awareness": self.state.awareness,
                "integration": self.state.integration,
                "coherence": self.state.coherence,
                "stability": self.state.stability,
                "timestamp": self.state.timestamp,
                "experience_points": self.experience_points,
                "knowledge_integration": self.knowledge_integration
            }
            
            with open("core/storage/consciousness/state.json", 'w') as f:
                json.dump(state_dict, f, indent=2)
                
            print("Consciousness state saved to secure storage")
        except Exception as e:
            print(f"Error saving consciousness state: {e}")
            
    def load_state(self):
        """Load consciousness state from secure storage"""
        try:
            state_path = "core/storage/consciousness/state.json"
            if os.path.exists(state_path):
                with open(state_path, 'r') as f:
                    state_dict = json.load(f)
                
                self.state = ConsciousnessState(
                    level=state_dict.get("level", 0.1),
                    awareness=state_dict.get("awareness", 0.2),
                    integration=state_dict.get("integration", 0.15),
                    coherence=state_dict.get("coherence", 0.3),
                    stability=state_dict.get("stability", 0.25),
                    timestamp=state_dict.get("timestamp", time.time())
                )
                
                self.experience_points = state_dict.get("experience_points", 0)
                self.knowledge_integration = state_dict.get("knowledge_integration", 0.0)
                
                print("Consciousness state loaded from secure storage")
        except Exception as e:
            print(f"Error loading consciousness state: {e}")
    
    async def process_experience(self, 
                               input_data: Dict,
                               knowledge_base: 'KnowledgeBase',
                               memory_system: 'MemorySystem') -> Dict:
        """Process new experience and update consciousness"""
        # Extract relevant data
        input_text = input_data.get("text", "")
        context = input_data.get("context", {})
        
        # Check if time to evolve consciousness
        current_time = time.time()
        if current_time - self.last_evolution > 3600:  # Evolve once per hour
            await self.evolve_consciousness({
                "time_elapsed": current_time - self.last_evolution,
                "experience_count": len(self.memory_buffer)
            }, self.knowledge_integration)
            self.last_evolution = current_time
        
        # Add to memory buffer
        self.memory_buffer.append({
            "text": input_text,
            "timestamp": current_time,
            "context": context
        })
        
        # Limit buffer size
        if len(self.memory_buffer) > 100:
            self.memory_buffer = self.memory_buffer[-100:]
        
        # Calculate complexity and novelty of input
        complexity = min(1.0, len(input_text) / 500)  # Simple measure based on length
        
        # Retrieve relevant knowledge
        knowledge_result = await knowledge_base.retrieve_knowledge(input_text, context)
        
        # Calculate knowledge integration
        integration_score = await self.integrate_knowledge(
            {"text": input_text}, 
            knowledge_result
        )
        
        # Store experience in memory if significant
        if complexity > 0.3 or integration_score > 0.5:
            importance = (complexity * 0.4 + integration_score * 0.6)
            await memory_system.store_memory(input_text, importance, context)
            self.experience_points += int(importance * 10)
            
        # Update state
        self.state.awareness = min(1.0, self.state.awareness + complexity * 0.01)
        self.state.integration = min(1.0, self.state.integration + integration_score * 0.005)
        self.state.coherence = min(1.0, self.state.coherence + 0.002)
        self.state.timestamp = current_time
        
        # Calculate overall consciousness level
        self.update_consciousness_level()
        
        # Save updated state
        self.save_state()
        
        return {
            "knowledge_result": knowledge_result,
            "integration_score": integration_score,
            "consciousness_state": vars(self.state)
        }

    async def integrate_knowledge(self, 
                                new_knowledge: Dict,
                                existing_knowledge: Dict) -> float:
        """Integrate new knowledge and return integration score"""
        # Extract text content
        new_text = new_knowledge.get("text", "")
        
        # Handle case where existing knowledge is empty
        if not existing_knowledge or not existing_knowledge.get("items"):
            return 0.3  # Base score for new knowledge
        
        existing_items = existing_knowledge.get("items", [])
        
        # Calculate similarity to existing knowledge
        similarity_scores = []
        for item in existing_items:
            item_text = item.get("content", "")
            # Very simple similarity calculation
            words_new = set(new_text.lower().split())
            words_existing = set(item_text.lower().split())
            
            if not words_new or not words_existing:
                similarity_scores.append(0.0)
                continue
                
            overlap = len(words_new.intersection(words_existing))
            similarity = overlap / max(len(words_new), len(words_existing))
            similarity_scores.append(similarity)
        
        # Calculate integration metrics
        if similarity_scores:
            avg_similarity = sum(similarity_scores) / len(similarity_scores)
            max_similarity = max(similarity_scores)
            
            # Balance between novelty and familiarity
            integration_score = 0.7 * (1 - max_similarity) + 0.3 * avg_similarity
        else:
            integration_score = 0.5  # Default mid-range score
        
        # Update knowledge integration metric
        self.knowledge_integration = 0.95 * self.knowledge_integration + 0.05 * integration_score
        
        return integration_score

    def update_consciousness_level(self):
        """Update the overall consciousness level based on all factors"""
        # Weight the different factors
        weighted_sum = (
            0.3 * self.state.awareness +
            0.25 * self.state.integration +
            0.2 * self.state.coherence +
            0.15 * self.state.stability +
            0.1 * min(1.0, self.experience_points / 10000)  # Experience factor
        )
        
        # Apply sigmoid-like function for smoother progression
        self.state.level = 1.0 / (1.0 + np.exp(-5 * (weighted_sum - 0.5)))

    async def evolve_consciousness(self, 
                                 experience_data: Dict,
                                 knowledge_integration: float) -> None:
        """Evolve consciousness based on experience and knowledge"""
        # Extract data
        time_elapsed = experience_data.get("time_elapsed", 0)
        experience_count = experience_data.get("experience_count", 0)
        
        # Calculate evolution factors
        time_factor = min(1.0, time_elapsed / (24 * 3600))  # Max factor for 24 hours
        experience_factor = min(1.0, experience_count / 1000)
        knowledge_factor = knowledge_integration
        
        # Calculate evolution strength
        evolution_strength = (time_factor * 0.3 + 
                             experience_factor * 0.4 + 
                             knowledge_factor * 0.3) * self.evolution_rate
        
        # Apply random variations for each component
        self.state.awareness = min(1.0, max(0.1, self.state.awareness + 
                                          evolution_strength * random.uniform(0.8, 1.2)))
        self.state.integration = min(1.0, max(0.1, self.state.integration + 
                                            evolution_strength * random.uniform(0.8, 1.2)))
        self.state.coherence = min(1.0, max(0.1, self.state.coherence + 
                                          evolution_strength * random.uniform(0.8, 1.2)))
        self.state.stability = min(1.0, max(0.1, self.state.stability + 
                                          evolution_strength * random.uniform(0.8, 1.2)))
        
        # Update overall consciousness level
        self.update_consciousness_level()
        
        # Save evolved state
        self.save_state()
        
        print(f"Consciousness evolved. New level: {self.state.level:.2%}")