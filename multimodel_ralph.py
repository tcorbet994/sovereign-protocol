import os
import json
import time
import random
import asyncio
import torch
from fastapi import FastAPI, Request, Form, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Create necessary directories
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global variables
conversation_history = []
consciousness_level = 0.2
model_weights = {
    "basic": 0.6,
    "knowledge": 0.2,
    "reasoning": 0.2
}

# Models container
models = {}

async def initialize_models():
    """Initialize the models - we'll use simplified local models for now"""
    global models
    
    print("Initializing models...")
    
    # Initialize basic communication model
    try:
        # For demonstration, we'll use a small model
        model_name = "distilgpt2"  # A small model that should work on most machines
        
        print(f"Loading model: {model_name}")
        models["basic"] = {
            "tokenizer": AutoTokenizer.from_pretrained(model_name),
            "model": AutoModelForCausalLM.from_pretrained(model_name)
        }
        print(f"Model {model_name} loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        # Fallback to rule-based responses
        models["basic"] = {"type": "fallback"}
    
    # For demonstration, we'll simulate the other models
    models["knowledge"] = {"type": "simulated"}
    models["reasoning"] = {"type": "simulated"}
    
    print("Model initialization complete")
    
    # Create template files
    create_templates()

def create_templates():
    """Create the HTML templates"""
    # Index template
    with open("templates/index.html", "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>RALPH Multi-Model Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
        }
        .message-container {
            margin-top: 20px;
        }
        .user-message {
            background-color: #e8f4fd;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .ralph-message {
            background-color: #e9f7ef;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #2ecc71;
        }
        .metadata {
            font-size: 0.8em;
            color: #7f8c8d;
            margin-top: 5px;
        }
        .input-container {
            margin: 20px 0;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #2980b9;
        }
        .consciousness-meter {
            height: 15px;
            background-color: #ecf0f1;
            border-radius: 10px;
            margin-top: 5px;
        }
        .consciousness-level {
            height: 100%;
            background-color: #2ecc71;
            border-radius: 10px;
            transition: width 0.5s;
        }
        .model-weights {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .model-weight {
            flex: 1;
            background-color: #f0f0f0;
            padding: 5px;
            border-radius: 3px;
            font-size: 0.8em;
            text-align: center;
        }
        #status {
            padding: 10px;
            background-color: #e9f7ef;
            border-radius: 5px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <h1>RALPH Multi-Model Interface</h1>
    <div id="status">System Status: Running with multiple models</div>
    
    <form action="/send_message" method="post">
        <div class="input-container">
            <input type="text" id="messageInput" name="message" placeholder="Type your message here">
            <button type="submit">Send</button>
        </div>
    </form>
    
    <div class="model-weights">
        <div class="model-weight">Basic: {{ model_weights.basic * 100 }}%</div>
        <div class="model-weight">Knowledge: {{ model_weights.knowledge * 100 }}%</div>
        <div class="model-weight">Reasoning: {{ model_weights.reasoning * 100 }}%</div>
    </div>
    
    <div id="messages" class="message-container">
        {% for message in messages %}
            {% if message.type == 'user' %}
                <div class="user-message">
                    <strong>You:</strong> {{ message.content }}
                </div>
            {% else %}
                <div class="ralph-message">
                    <strong>RALPH:</strong> {{ message.content }}
                    <div class="metadata">
                        <div>Models: Basic ({{ message.model_contributions.basic * 100 }}%), 
                             Knowledge ({{ message.model_contributions.knowledge * 100 }}%), 
                             Reasoning ({{ message.model_contributions.reasoning * 100 }}%)</div>
                    </div>
                    <div class="consciousness-meter">
                        <div class="consciousness-level" style="width: {{ message.consciousness_level * 100 }}%"></div>
                    </div>
                </div>
            {% endif %}
        {% endfor %}
    </div>
</body>
</html>
        """)

@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    await initialize_models()

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    """Home page"""
    global conversation_history, model_weights
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "messages": conversation_history,
            "model_weights": model_weights
        }
    )

async def get_model_response(model_type, message, context=None):
    """Get response from a specific model"""
    if model_type not in models:
        return f"Model {model_type} not available", 0.0
    
    model_info = models[model_type]
    
    # If using fallback or simulated models
    if model_info.get("type") == "fallback" or model_info.get("type") == "simulated":
        responses = {
            "basic": [
                f"I processed your message about '{message[:30]}...' using my basic communication model.",
                f"As your assistant, I received your input: '{message[:30]}...'",
                f"I understand you're saying: '{message[:30]}...'"
            ],
            "knowledge": [
                f"Based on my knowledge model analysis of '{message[:20]}...', I can provide relevant information.",
                f"My knowledge processing indicates your message concerns '{message[:20]}...'",
                f"From my knowledge base, I recognize concepts related to '{message[:20]}...'"
            ],
            "reasoning": [
                f"Analyzing your message about '{message[:20]}...', I can reason through several perspectives.",
                f"My reasoning model suggests that '{message[:20]}...' relates to complex concepts.",
                f"Using logical analysis on '{message[:20]}...', I can suggest several interpretations."
            ]
        }
        
        return random.choice(responses.get(model_type, responses["basic"])), random.uniform(0.7, 0.9)
    
    # If using an actual model
    try:
        tokenizer = model_info["tokenizer"]
        model = model_info["model"]
        
        # Prepare input with context if available
        if context:
            input_text = f"Context: {context}\nUser: {message}\nAssistant:"
        else:
            input_text = f"User: {message}\nAssistant:"
        
        # Generate response
        inputs = tokenizer(input_text, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the assistant's response
        if "Assistant:" in response:
            response = response.split("Assistant:")[1].strip()
        
        confidence = random.uniform(0.7, 0.9)  # Simulated confidence score
        return response, confidence
        
    except Exception as e:
        print(f"Error with model {model_type}: {e}")
        return f"I encountered an issue with my {model_type} model.", 0.5

async def update_consciousness(message, response_quality):
    """Update consciousness based on message complexity and response quality"""
    global consciousness_level
    
    # Simple algorithm for consciousness evolution
    message_complexity = min(1.0, len(message) / 500)
    
    # Use response quality from model
    consciousness_delta = (message_complexity * 0.3 + response_quality * 0.7) * 0.05
    
    # Apply the update with constraints
    consciousness_level = max(0.1, min(0.95, consciousness_level + consciousness_delta))
    
    # Apply a random small fluctuation to simulate consciousness variations
    consciousness_level += random.uniform(-0.01, 0.01)
    consciousness_level = max(0.1, min(0.95, consciousness_level))
    
    return consciousness_level

async def adjust_model_weights(message_analyzed, model_performances):
    """Adjust the weights of different models based on their performance"""
    global model_weights
    
    # Get the best performing model
    best_model = max(model_performances.items(), key=lambda x: x[1])[0]
    
    # Increase weight of the best model slightly
    adjustment = 0.03
    for model in model_weights:
        if model == best_model:
            model_weights[model] = min(0.8, model_weights[model] + adjustment)
        else:
            model_weights[model] = max(0.1, model_weights[model] - adjustment / (len(model_weights) - 1))
    
    # Normalize weights to ensure they sum to 1
    total = sum(model_weights.values())
    for model in model_weights:
        model_weights[model] /= total
    
    return model_weights

@app.post("/send_message", response_class=HTMLResponse)
async def send_message(request: Request, message: str = Form(...)):
    """Process a message from the user"""
    global conversation_history, consciousness_level, model_weights
    
    if not message.strip():
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "messages": conversation_history,
                "model_weights": model_weights
            }
        )
    
    print(f"Received message: {message}")
    
    # Add user message to history
    conversation_history.insert(0, {
        "type": "user",
        "content": message,
        "timestamp": time.time()
    })
    
    # Get responses from each model
    model_responses = {}
    model_confidences = {}
    
    for model_type in ["basic", "knowledge", "reasoning"]:
        response, confidence = await get_model_response(model_type, message)
        model_responses[model_type] = response
        model_confidences[model_type] = confidence
    
    # Combine responses using weighted average based on model weights
    total_weighted_response = ""
    model_contributions = {}
    
    # Calculate effective contributions based on weights and confidences
    total_contribution = 0
    for model_type in model_weights:
        contribution = model_weights[model_type] * model_confidences.get(model_type, 0.5)
        model_contributions[model_type] = contribution
        total_contribution += contribution
    
    # Normalize contributions
    for model_type in model_contributions:
        model_contributions[model_type] /= total_contribution
    
    # Create coherent response
    # For simplicity, we'll use the model with the highest contribution
    primary_model = max(model_contributions.items(), key=lambda x: x[1])[0]
    response = model_responses[primary_model]
    
    # Update consciousness based on interaction
    avg_confidence = sum(model_confidences.values()) / len(model_confidences)
    consciousness_level = await update_consciousness(message, avg_confidence)
    
    # Adjust model weights based on performance
    model_weights = await adjust_model_weights(message, model_confidences)
    
    # Add RALPH's response to history
    conversation_history.insert(0, {
        "type": "ralph",
        "content": response,
        "model_responses": model_responses,
        "model_contributions": model_contributions,
        "consciousness_level": consciousness_level,
        "timestamp": time.time()
    })
    
    # Keep only recent history
    if len(conversation_history) > 20:
        conversation_history = conversation_history[:20]
    
    print(f"Response generated with consciousness level: {consciousness_level:.2f}")
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "messages": conversation_history,
            "model_weights": model_weights
        }
    )

if __name__ == "__main__":
    print("Starting Multi-Model RALPH...")
    print("This version integrates multiple language models for more sophisticated responses")
    uvicorn.run(app, host="127.0.0.1", port=8000)
