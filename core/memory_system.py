from typing import Dict, List, Optional, Union, Any
import json
import os
import time
import torch
import numpy as np
from datetime import datetime

class Memory:
    def __init__(self, content: str, importance: float, context: Optional[Dict] = None):
        self.content = content
        self.importance = importance
        self.context = context or {}
        self.timestamp = time.time()
        self.access_count = 0
        self.last_access = self.timestamp
        self.embedding = None
    
    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "importance": self.importance,
            "context": self.context,
            "timestamp": self.timestamp,
            "access_count": self.access_count,
            "last_access": self.last_access
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        memory = cls(data["content"], data["importance"], data["context"])
        memory.timestamp = data["timestamp"]
        memory.access_count = data["access_count"]
        memory.last_access = data["last_access"]
        return memory

class MemorySystem:
    def __init__(self, embedding_model: Any, storage_path: str = "core/storage/memories"):
        self.memories: List[Memory] = []
        self.embedding_model = embedding_model
        self.storage_path = storage_path
        self.ensure_storage_path()
        self.load_memories()
    
    def ensure_storage_path(self) -> None:
        """Ensure the storage directory exists"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def load_memories(self) -> None:
        """Load memories from storage"""
        try:
            memory_file = os.path.join(self.storage_path, "memories.json")
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                    self.memories = [Memory.from_dict(m) for m in memory_data]
                print(f"Loaded {len(self.memories)} memories from storage")
        except Exception as e:
            print(f"Error loading memories: {e}")
    
    def save_memories(self) -> None:
        """Save memories to storage"""
        try:
            memory_file = os.path.join(self.storage_path, "memories.json")
            with open(memory_file, 'w') as f:
                memory_data = [m.to_dict() for m in self.memories]
                json.dump(memory_data, f, indent=2)
            print(f"Saved {len(self.memories)} memories to storage")
        except Exception as e:
            print(f"Error saving memories: {e}")
    
    async def store_memory(self, content: str, importance: float, context: Optional[Dict] = None) -> Memory:
        """Store a new memory"""
        memory = Memory(content, importance, context)
        memory.embedding = await self.generate_embedding(content)
        self.memories.append(memory)
        self.save_memories()
        return memory
    
    async def retrieve_relevant_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """Retrieve memories relevant to the query"""
        if not self.memories:
            return []
        
        query_embedding = await self.generate_embedding(query)
        
        # Calculate relevance scores
        relevance_scores = []
        for memory in self.memories:
            if memory.embedding is None:
                memory.embedding = await self.generate_embedding(memory.content)
            
            # Cosine similarity
            similarity = torch.nn.functional.cosine_similarity(
                query_embedding.unsqueeze(0), 
                memory.embedding.unsqueeze(0)
            ).item()
            
            # Adjust by importance and recency
            recency_factor = 1.0 / (1.0 + 0.1 * (time.time() - memory.timestamp) / 86400)  # Days factor
            score = similarity * 0.6 + memory.importance * 0.3 + recency_factor * 0.1
            
            relevance_scores.append((memory, score))
        
        # Sort by relevance score
        relevance_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Update access stats
        for memory, _ in relevance_scores[:limit]:
            memory.access_count += 1
            memory.last_access = time.time()
        
        self.save_memories()
        return [memory for memory, _ in relevance_scores[:limit]]
    
    async def forget_memory(self, memory_id: int) -> bool:
        """Remove a memory by index"""
        if 0 <= memory_id < len(self.memories):
            self.memories.pop(memory_id)
            self.save_memories()
            return True
        return False
    
    async def generate_embedding(self, text: str) -> torch.Tensor:
        """Generate embedding for text using the embedding model"""
        try:
            # This can be customized based on the embedding model you're using
            input_ids = self.embedding_model.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).input_ids
            with torch.no_grad():
                embeddings = self.embedding_model.model(input_ids).last_hidden_state.mean(dim=1)
            return embeddings[0]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            # Return a random embedding as fallback
            return torch.randn(768)
