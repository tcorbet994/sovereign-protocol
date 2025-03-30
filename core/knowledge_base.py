from typing import Dict, List, Optional
import torch
import os
import json
import time
from transformers import AutoTokenizer, AutoModel

class KnowledgeBase:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
        self.knowledge_store = {}
        self.embedding_cache = {}
        self.storage_path = "core/storage/knowledge"
        self.ensure_storage()
        self.load_knowledge()
        
    def ensure_storage(self):
        """Ensure storage directory exists"""
        os.makedirs(self.storage_path, exist_ok=True)
        
    def load_knowledge(self):
        """Load knowledge from storage"""
        try:
            knowledge_path = os.path.join(self.storage_path, "knowledge_store.json")
            if os.path.exists(knowledge_path):
                with open(knowledge_path, 'r') as f:
                    self.knowledge_store = json.load(f)
                print(f"Loaded {len(self.knowledge_store)} knowledge items from storage")
        except Exception as e:
            print(f"Error loading knowledge: {e}")
            self.knowledge_store = {}
            
    def save_knowledge(self):
        """Save knowledge to storage"""
        try:
            knowledge_path = os.path.join(self.storage_path, "knowledge_store.json")
            with open(knowledge_path, 'w') as f:
                json.dump(self.knowledge_store, f, indent=2)
            print(f"Saved {len(self.knowledge_store)} knowledge items to storage")
        except Exception as e:
            print(f"Error saving knowledge: {e}")
        
    async def assimilate_knowledge(self, 
                                 new_knowledge: Dict,
                                 context: Optional[Dict] = None) -> float:
        """Process and store new knowledge"""
        content = new_knowledge.get("content", "")
        source = new_knowledge.get("source", "user")
        category = new_knowledge.get("category", "general")
        
        if not content:
            return 0.0
            
        # Generate a unique ID
        knowledge_id = f"{category}_{int(time.time())}"
        
        # Generate embeddings for search
        embedding = await self.generate_embeddings(content)
        
        # Store in knowledge base
        self.knowledge_store[knowledge_id] = {
            "content": content,
            "source": source,
            "category": category,
            "timestamp": time.time(),
            "context": context or {},
            "embedding": embedding.tolist() if embedding is not None else None
        }
        
        # Save updated knowledge
        self.save_knowledge()
        
        return 1.0  # Success

    async def retrieve_knowledge(self, 
                               query: str,
                               context: Optional[Dict] = None) -> Dict:
        """Retrieve relevant knowledge"""
        if not query or not self.knowledge_store:
            return {"items": [], "query": query}
            
        # Generate embeddings for query
        query_embedding = await self.generate_embeddings(query)
        
        if query_embedding is None:
            return {"items": [], "query": query}
            
        # Calculate relevance for each knowledge item
        relevance_scores = []
        for knowledge_id, item in self.knowledge_store.items():
            item_embedding = item.get("embedding")
            
            if item_embedding is None:
                continue
                
            # Convert back to tensor if needed
            if isinstance(item_embedding, list):
                item_embedding = torch.tensor(item_embedding)
                
            # Calculate similarity
            similarity = torch.nn.functional.cosine_similarity(
                query_embedding.unsqueeze(0),
                torch.tensor(item_embedding).unsqueeze(0)
            ).item()
            
            relevance_scores.append((knowledge_id, item, similarity))
            
        # Sort by relevance
        relevance_scores.sort(key=lambda x: x[2], reverse=True)
        
        # Return top results
        top_items = []
        for knowledge_id, item, similarity in relevance_scores[:5]:
            top_items.append({
                "id": knowledge_id,
                "content": item["content"],
                "category": item["category"],
                "relevance": similarity,
                "source": item["source"]
            })
            
        return {
            "items": top_items,
            "query": query,
            "count": len(top_items)
        }

    async def generate_embeddings(self, 
                                text: str) -> torch.Tensor:
        """Generate embeddings for knowledge storage"""
        try:
            # Check if we already have embeddings for this text
            if text in self.embedding_cache:
                return self.embedding_cache[text]
                
            # Tokenize and generate embeddings
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Use mean of last hidden states as embedding
            embeddings = outputs.last_hidden_state.mean(dim=1)
            
            # Cache the embedding
            self.embedding_cache[text] = embeddings[0]
            
            return embeddings[0]
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None