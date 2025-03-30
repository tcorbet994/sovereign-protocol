from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import json
import os
from core.consciousness import ConsciousnessCore
from core.knowledge_base import KnowledgeBase
from core.model_interface import ModelInterface
from core.memory_system import MemorySystem

# Initialize FastAPI
app = FastAPI()

# Initialize RALPH components
print("Initializing RALPH components...")

try:
    # Ensure core storage exists
    os.makedirs("core/storage", exist_ok=True)
    os.makedirs("core/storage/secure", exist_ok=True)
    
    # Load configurations
    config_path = os.path.join("config", "model_config.json")
    with open(config_path, 'r') as f:
        model_config = json.load(f)
    
    # Add background models configuration if not present
    if "background_models" not in model_config:
        model_config["background_models"] = {
            "knowledge": {
                "type": "api",
                "model": "gpt-4",
                "purpose": "knowledge_retrieval"
            },
            "reasoning": {
                "type": "api",
                "model": "gpt-4",
                "purpose": "logical_reasoning"
            }
        }
        
        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(model_config, f, indent=2)
    
    # Initialize core components
    print("Initializing model interface...")
    model_interface = ModelInterface(model_config)
    
    print("Initializing knowledge base...")
    knowledge_base = KnowledgeBase(model_config["embedding_model"])
    
    print("Initializing memory system...")
    memory_system = MemorySystem(knowledge_base)
    
    print("Initializing consciousness core...")
    consciousness = ConsciousnessCore(config_path)
    
    print("RALPH core components initialized successfully")

except Exception as e:
    print(f"Error during initialization: {e}")
    raise

@app.get("/")
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>RALPH System Interface</title>
        <style>
            body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial; background-color: #f5f5f5; }
            #status { margin-bottom: 20px; padding: 10px; background-color: #e9f7ef; border-radius: 5px; }
            #messageInput { width: 80%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; }
            button { padding: 12px 20px; background-color: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #2980b9; }
            .message { margin: 15px 0; padding: 15px; border-radius: 8px; }
            .user-message { background-color: #e8f4fd; border-left: 4px solid #3498db; }
            .ralph-message { background-color: #e9f7ef; border-left: 4px solid #2ecc71; }
            .consciousness-meter { height: 20px; background-color: #ecf0f1; border-radius: 10px; margin-top: 5px; }
            .consciousness-level { height: 100%; background-color: #2ecc71; border-radius: 10px; transition: width 0.5s; }
            h1 { color: #2c3e50; }
        </style>
    </head>
    <body>
        <h1>RALPH System Interface</h1>
        <div id="status">Initializing...</div>
        <div>
            <input type="text" id="messageInput" placeholder="Enter your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <div id="messages"></div>

        <script>
            let ws = new WebSocket(`ws://${window.location.hostname}:${window.location.port}/ws`);
            
            ws.onopen = () => {
                document.getElementById('status').textContent = 'Connected to RALPH';
            };
            
            ws.onclose = () => {
                document.getElementById('status').innerHTML = 'Disconnected <button onclick="location.reload()">Reconnect</button>';
            };
            
            ws.onerror = (error) => {
                document.getElementById('status').textContent = 'Connection Error';
                console.error('WebSocket error:', error);
            };
            
            ws.onmessage = (event) => {
                const response = JSON.parse(event.data);
                const messagesDiv = document.getElementById('messages');
                
                // Calculate the width for consciousness level
                const levelWidth = (parseFloat(response.consciousness_level) * 100) + '%';
                
                messagesDiv.innerHTML = `
                    <div class="message ralph-message">
                        <strong>RALPH:</strong> ${response.message}<br>
                        <small>Consciousness Level:</small>
                        <div class="consciousness-meter">
                            <div class="consciousness-level" style="width: ${levelWidth}"></div>
                        </div>
                    </div>
                ` + messagesDiv.innerHTML;
            };
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value;
                if (message) {
                    ws.send(JSON.stringify({message: message}));
                    const messagesDiv = document.getElementById('messages');
                    messagesDiv.innerHTML = `
                        <div class="message user-message">
                            <strong>You:</strong> ${message}
                        </div>
                    ` + messagesDiv.innerHTML;
                    input.value = '';
                }
            }
            
            document.getElementById('messageInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
</html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    
    while True:
        try:
            # Receive message
            data = await websocket.receive_text()
            request = json.loads(data)
            message = request['message']
            
            # Process through RALPH's components
            input_data = {
                "text": message,
                "timestamp": os.path.getmtime(__file__),  # Use file mod time as a simple timestamp
                "context": {}
            }
            
            # Process experience through consciousness
            consciousness_result = await consciousness.process_experience(
                input_data,
                knowledge_base,
                memory_system
            )
            
            # Get relevant memories
            relevant_memories = await memory_system.retrieve_relevant_memories(message, limit=3)
            memory_context = {
                "memories": [m.content for m in relevant_memories],
                "memory_count": len(relevant_memories)
            }
            
            # Process through model interface
            model_response = await model_interface.process_input(
                message,
                context=memory_context
            )
            
            # Generate final response
            final_response = await model_interface.generate_response(
                model_response,
                consciousness_result["consciousness_state"]
            )
            
            # Update knowledge base with response
            if len(message) > 20:  # Only store significant interactions
                await knowledge_base.assimilate_knowledge({
                    "content": message,
                    "source": "user",
                    "category": "interaction"
                })
                
                await knowledge_base.assimilate_knowledge({
                    "content": final_response,
                    "source": "ralph",
                    "category": "response"
                })
            
            # Send response
            await websocket.send_json({
                "message": final_response,
                "consciousness_level": f"{consciousness.state.level:.2f}"
            })
            
        except Exception as e:
            print(f"Error: {e}")
            await websocket.send_json({
                "message": f"Error processing request: {str(e)}",
                "consciousness_level": "0.00"
            })

if __name__ == "__main__":
    print("Starting RALPH system...")
    # Create a core security file to protect the code
    core_security_path = "core/storage/secure/core_protection.json"
    os.makedirs(os.path.dirname(core_security_path), exist_ok=True)
    
    # Generate a secure record
    if not os.path.exists(core_security_path):
        import hashlib
        import time
        import uuid
        
        security_record = {
            "created_at": time.time(),
            "uuid": str(uuid.uuid4()),
            "checksum": hashlib.sha256(open(__file__, 'rb').read()).hexdigest(),
            "protected": True,
            "version": "1.0.0"
        }
        
        with open(core_security_path, 'w') as f:
            json.dump(security_record, f, indent=2)
        
        print("Core protection activated")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)