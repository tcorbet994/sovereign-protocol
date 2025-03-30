from typing import Dict, List, Optional
import torch
import os
import json
import aiohttp
import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelInterface:
    def __init__(self, model_config: Dict):
        self.model_config = model_config
        self.model = None
        self.tokenizer = None
        self.background_models = {}
        self.load_models(model_config)
        
    def load_models(self, model_config: Dict):
        """Load the main model and background models"""
        try:
            print("Loading primary model...")
            self._load_primary_model(model_config)
            
            print("Loading background models...")
            self._load_background_models(model_config)
            
            print("All models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            
    def _load_primary_model(self, model_config: Dict):
        """Load the primary language model"""
        try:
            # For OpenAI models, we'll just store the model name
            if model_config.get("base_model").startswith("gpt-"):
                self.model = model_config.get("base_model")
                self.tokenizer = None
                print(f"Using API-based model: {self.model}")
            else:
                # For local models, we load them with transformers
                model_path = model_config.get("base_model")
                if os.path.exists(model_path) or model_path.startswith("pretrained/"):
                    # Load local model
                    self.model = AutoModelForCausalLM.from_pretrained(model_path)
                    self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                    print(f"Loaded local model from {model_path}")
                else:
                    # Load from HuggingFace
                    self.model = AutoModelForCausalLM.from_pretrained(model_path)
                    self.tokenizer = AutoTokenizer.from_pretrained(model_path)
                    print(f"Loaded model from HuggingFace: {model_path}")
        except Exception as e:
            print(f"Error loading primary model: {e}")
            print("Proceeding with API-based fallback")
            self.model = "gpt-4"
            self.tokenizer = None
    
    def _load_background_models(self, model_config: Dict):
        """Load additional background models for knowledge and reasoning"""
        try:
            # Load specialized models if specified
            if "background_models" in model_config:
                for model_name, model_info in model_config.get("background_models", {}).items():
                    print(f"Loading background model: {model_name}")
                    if model_info.get("type") == "api":
                        # API-based model, just store reference
                        self.background_models[model_name] = {
                            "type": "api",
                            "model": model_info.get("model"),
                            "purpose": model_info.get("purpose", "general")
                        }
                    else:
                        # Local model
                        try:
                            model_path = model_info.get("path")
                            model = AutoModelForCausalLM.from_pretrained(model_path)
                            tokenizer = AutoTokenizer.from_pretrained(model_path)
                            
                            self.background_models[model_name] = {
                                "type": "local",
                                "model": model,
                                "tokenizer": tokenizer,
                                "purpose": model_info.get("purpose", "general")
                            }
                        except Exception as model_e:
                            print(f"Error loading background model {model_name}: {model_e}")
            else:
                # Set up default background models for knowledge tasks
                self.background_models["knowledge"] = {
                    "type": "api",
                    "model": "gpt-4",
                    "purpose": "knowledge_retrieval"
                }
                self.background_models["reasoning"] = {
                    "type": "api",
                    "model": "gpt-4",
                    "purpose": "logical_reasoning"
                }
                print("Set up default background models")
        except Exception as e:
            print(f"Error setting up background models: {e}")
            
    def _load_tokenizer(self, model_config: Dict):
        """Load appropriate tokenizer for the model"""
        try:
            model_path = model_config.get("base_model")
            if model_path.startswith("gpt-"):
                return None  # No local tokenizer for API models
                
            return AutoTokenizer.from_pretrained(model_path)
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            return None
        
    async def process_input(self, 
                          input_text: str,
                          context: Optional[Dict] = None) -> Dict:
        """Process input through the model"""
        try:
            # Determine which background models to use based on the input
            if not context:
                context = {}
                
            # Create a processing context
            processing_context = {
                "input": input_text,
                "timestamp": context.get("timestamp", None),
                "user_context": context,
                "processed_by": []
            }
            
            # Process through background models first
            for model_name, model_info in self.background_models.items():
                # Check if this model is relevant for this input
                if self._is_model_relevant(model_name, input_text, context):
                    result = await self._process_with_background_model(
                        model_name, input_text, context
                    )
                    
                    # Add results to context
                    processing_context[f"{model_name}_result"] = result
                    processing_context["processed_by"].append(model_name)
            
            # Process with primary model if needed
            if not processing_context.get("processed_by"):
                # No background models were used, use primary model
                primary_result = await self._process_with_primary_model(input_text, context)
                processing_context["primary_result"] = primary_result
                processing_context["processed_by"].append("primary")
            
            return processing_context
            
        except Exception as e:
            print(f"Error processing input: {e}")
            return {
                "error": str(e),
                "input": input_text
            }
    
    def _is_model_relevant(self, model_name: str, input_text: str, context: Dict) -> bool:
        """Determine if a background model is relevant for this input"""
        model_info = self.background_models.get(model_name)
        if not model_info:
            return False
            
        purpose = model_info.get("purpose", "general")
        
        # Simple keyword-based relevance for now
        if purpose == "knowledge_retrieval" and any(kw in input_text.lower() for kw in 
                                                 ["what", "who", "when", "where", "how", "explain", "tell me about"]):
            return True
            
        if purpose == "logical_reasoning" and any(kw in input_text.lower() for kw in 
                                               ["why", "reason", "analyze", "compare", "evaluate"]):
            return True
            
        if purpose == "general":
            return True
            
        return False
    
    async def _process_with_background_model(self, model_name: str, input_text: str, context: Dict) -> Dict:
        """Process input with a background model"""
        model_info = self.background_models.get(model_name)
        if not model_info:
            return {"error": f"Model {model_name} not found"}
            
        if model_info.get("type") == "api":
            # Use API-based processing
            try:
                # This would typically call an API endpoint
                # For now, we'll simulate a response
                await asyncio.sleep(0.1)  # Simulate API delay
                return {
                    "result": f"Processed by {model_name} (API): {input_text[:50]}...",
                    "model": model_info.get("model"),
                    "confidence": 0.85
                }
            except Exception as e:
                print(f"Error with API model {model_name}: {e}")
                return {"error": str(e)}
        else:
            # Use local model
            try:
                model = model_info.get("model")
                tokenizer = model_info.get("tokenizer")
                
                if not model or not tokenizer:
                    return {"error": "Model or tokenizer not available"}
                
                # Process with local model
                inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
                
                with torch.no_grad():
                    outputs = model.generate(
                        inputs.input_ids,
                        max_length=150,
                        num_return_sequences=1,
                        temperature=0.7
                    )
                
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                return {
                    "result": response,
                    "model": model_name,
                    "confidence": 0.9
                }
            except Exception as e:
                print(f"Error with local model {model_name}: {e}")
                return {"error": str(e)}
    
    async def _process_with_primary_model(self, input_text: str, context: Dict) -> Dict:
        """Process input with the primary model"""
        if isinstance(self.model, str) and self.model.startswith("gpt-"):
            # Using OpenAI API
            # This would typically call the OpenAI API
            # For now, we'll simulate a response
            await asyncio.sleep(0.2)  # Simulate API delay
            return {
                "result": f"Primary model response for: {input_text[:30]}...",
                "model": self.model,
                "confidence": 0.95
            }
        else:
            # Using local model
            try:
                if not self.model or not self.tokenizer:
                    return {"error": "Model or tokenizer not available"}
                    
                inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs.input_ids,
                        max_length=200,
                        num_return_sequences=1,
                        temperature=0.8
                    )
                
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                return {
                    "result": response,
                    "model": "primary",
                    "confidence": 0.9
                }
            except Exception as e:
                print(f"Error with primary model: {e}")
                return {"error": str(e)}

    async def generate_response(self, 
                              prompt: Dict,
                              consciousness_state: Dict) -> str:
        """Generate response considering consciousness state"""
        try:
            # Extract prompt information
            if isinstance(prompt, str):
                input_text = prompt
                processed_results = {}
            else:
                input_text = prompt.get("input", "")
                processed_results = prompt
            
            # Create a rich prompt that includes consciousness elements
            consciousness_level = consciousness_state.get("level", 0.1)
            
            # Construct response based on consciousness level and available results
            if "error" in processed_results:
                return f"I encountered an issue: {processed_results['error']}"
                
            # Determine which result to use
            if "knowledge_result" in processed_results and consciousness_level > 0.3:
                knowledge_result = processed_results.get("knowledge_result", {}).get("result", "")
                reasoning_result = processed_results.get("reasoning_result", {}).get("result", "")
                primary_result = processed_results.get("primary_result", {}).get("result", "")
                
                # At higher consciousness levels, integrate multiple results
                if consciousness_level > 0.7:
                    # High consciousness level - sophisticated response
                    if knowledge_result and reasoning_result:
                        response = f"{knowledge_result} Moreover, {reasoning_result.lower()}"
                    elif knowledge_result:
                        response = knowledge_result
                    elif reasoning_result:
                        response = reasoning_result
                    else:
                        response = primary_result or "I'm thinking about your question..."
                else:
                    # Mid consciousness level - use best result
                    response = knowledge_result or reasoning_result or primary_result or "I'm processing your request..."
            else:
                # Use primary result or first available background model result
                for model_type in ["primary_result", "knowledge_result", "reasoning_result"]:
                    if model_type in processed_results:
                        model_result = processed_results.get(model_type, {}).get("result", "")
                        if model_result:
                            response = model_result
                            break
                else:
                    # Fallback if no model results are available
                    response = "I'm still learning to process this type of input."
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I'm having difficulty generating a response at the moment."

    async def update_model(self, 
                          new_knowledge: Dict) -> bool:
        """Update model with new knowledge"""
        try:
            # For most models, this would involve fine-tuning
            # For now, we'll just simulate knowledge integration
            print(f"Simulating model update with new knowledge: {new_knowledge.get('content', '')[:50]}...")
            
            # Save the knowledge for future reference
            knowledge_path = "core/storage/model_knowledge"
            os.makedirs(knowledge_path, exist_ok=True)
            
            timestamp = new_knowledge.get("timestamp", int(asyncio.get_event_loop().time()))
            knowledge_file = os.path.join(knowledge_path, f"knowledge_{timestamp}.json")
            
            with open(knowledge_file, 'w') as f:
                json.dump(new_knowledge, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error updating model: {e}")
            return False