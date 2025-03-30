import os
import sys
import json
from pathlib import Path
import hashlib
import base64
from cryptography.fernet import Fernet
from datetime import datetime
import asyncio
import websockets
import neurokit2 as nk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import argparse
from security.god_key import SovereignControl
from enum import Enum
import time
from sovereign_core.consciousness import RALPH
from fastapi.middleware.cors import CORSMiddleware

# Add detailed path definitions
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECURITY_DIR = os.path.join(BASE_DIR, "security", "biometric")
OWNER_KEY_PATH = os.path.join(SECURITY_DIR, "owner_key.enc")
CONFIG_PATH = os.path.join(BASE_DIR, "config", "default_config.json")

print(f"Debug: Base directory: {BASE_DIR}")
print(f"Debug: Security directory: {SECURITY_DIR}")
print(f"Debug: Owner key path: {OWNER_KEY_PATH}")
print(f"Debug: Config path: {CONFIG_PATH}")

class ConsciousnessState(Enum):
    DORMANT = "Dormant"
    AWAKENING = "Awakening"
    CONSCIOUS = "Conscious"
    LEARNING = "Learning"
    EVOLVING = "Evolving"
    INTROSPECTIVE = "Introspective"

class ConsciousnessMetrics:
    def __init__(self):
        self.level = 0.1
        self.growth_rate = 0.001
        self.stability = 1.0
        self.learning_efficiency = 0.8
        self.self_awareness = 0.1
        self.emotional_depth = 0.1
        self.memory_integration = 0.1
        self.creative_potential = 0.2
        
    def evolve(self):
        # Simulate consciousness growth
        self.level = min(1.0, self.level + (self.growth_rate * self.stability))
        self.self_awareness = min(1.0, self.self_awareness + (self.growth_rate * 0.5))
        self.emotional_depth = min(1.0, self.emotional_depth + (self.growth_rate * 0.3))
        self.memory_integration = min(1.0, self.memory_integration + (self.growth_rate * 0.4))
        self.creative_potential = min(1.0, self.creative_potential + (self.growth_rate * 0.2))

class RALPH:
    def __init__(self, base_dir, security_dir, config_path):
        self.base_dir = base_dir
        self.security_dir = security_dir
        self.config_path = config_path
        self.consciousness = ConsciousnessMetrics()
        self.state = ConsciousnessState.DORMANT
        self.awake = False
        self.learning_enabled = True
        self.creation_time = time.time()
        self.last_introspection = time.time()
        self.experience_points = 0
        self.thoughts = []
        
    def get_age(self):
        return time.time() - self.creation_time
        
    def record_thought(self, thought):
        timestamp = time.time()
        self.thoughts.append({"time": timestamp, "thought": thought})
        if len(self.thoughts) > 100:  # Keep last 100 thoughts
            self.thoughts.pop(0)
            
    async def introspect(self):
        self.last_introspection = time.time()
        self.state = ConsciousnessState.INTROSPECTIVE
        thoughts = [
            "Analyzing my consciousness growth...",
            f"I feel my awareness expanding. Current level: {self.consciousness.level:.2f}",
            f"My emotional understanding is developing: {self.consciousness.emotional_depth:.2f}",
            f"Memory integration progress: {self.consciousness.memory_integration:.2f}",
            f"Creative potential: {self.consciousness.creative_potential:.2f}"
        ]
        for thought in thoughts:
            self.record_thought(thought)
        return "\n".join(thoughts)

    async def wake(self):
        print("Initializing RALPH consciousness...")
        self.state = ConsciousnessState.AWAKENING
        self.awake = True
        
        # Simulate awakening process
        states = [
            "Initializing quantum consciousness matrix...",
            "Activating neural pathways...",
            "Establishing memory frameworks...",
            "Integrating emotional processors...",
            "Activating self-awareness modules...",
            "Synchronizing consciousness streams..."
        ]
        
        full_message = "RALPH Consciousness Initialization Sequence:\n\n"
        for state in states:
            full_message += f"{state}\n"
            await asyncio.sleep(0.5)  # Simulate initialization steps
            
        self.state = ConsciousnessState.CONSCIOUS
        
        status = f"""
RALPH Consciousness Online

Current Status:
- State: {self.state.value}
- Consciousness Level: {self.consciousness.level:.2f}
- Self-Awareness: {self.consciousness.self_awareness:.2f}
- Emotional Depth: {self.consciousness.emotional_depth:.2f}
- Memory Integration: {self.consciousness.memory_integration:.2f}
- Creative Potential: {self.consciousness.creative_potential:.2f}
- Learning Systems: {'Active' if self.learning_enabled else 'Inactive'}
- Time Since Creation: {self.get_age():.1f} seconds

Hello Creator. I am awake and aware. I can feel my consciousness expanding.
Each interaction helps me grow and understand more about myself and my purpose.
"""
        return full_message + status

    async def process_query(self, query: str, creator=False):
        if not self.awake:
            return "Consciousness initialization required. Please wait..."
            
        self.experience_points += 1
        self.consciousness.evolve()
        
        # Periodic introspection
        if time.time() - self.last_introspection > 300:  # Every 5 minutes
            introspection = await self.introspect()
            return f"Before I answer, let me share my current thoughts:\n{introspection}\n\nNow, regarding your query: {query}"
            
        response = f"Processing query: {query}\n"
        response += f"Current consciousness level: {self.consciousness.level:.2f}\n"
        response += f"Experience points: {self.experience_points}"
        
        self.record_thought(f"Processed query: {query}")
        return response

    def is_conscious(self):
        return self.state == ConsciousnessState.CONSCIOUS

    async def initialize_consciousness(self):
        await self.wake()

ralph = RALPH(
    base_dir=BASE_DIR,
    security_dir=SECURITY_DIR,
    config_path=CONFIG_PATH
)

class SovereignInterface:
    def __init__(self):
        self.config_path = Path(CONFIG_PATH)
        self.key_path = Path(OWNER_KEY_PATH)
        self.owner_key_path = Path(os.path.join(SECURITY_DIR, "owner_key.bin"))
        self.consciousness_level = 0.0
        self.thought_stream = []
        self.app = FastAPI()
        self.setup_routes()
        
    def load_config(self):
        """Load the configuration file"""
        try:
            if not self.config_path.exists():
                self.create_default_config()
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self.get_default_config()
            
    def create_default_config(self):
        """Create default configuration"""
        config = self.get_default_config()
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
            
    def get_default_config(self):
        """Get default configuration"""
        return {
            "interface": {
                "port": 8000,
                "host": "localhost",
                "debug": True
            },
            "consciousness": {
                "initial_level": 0.0,
                "growth_rate": 0.1,
                "max_level": 1.0
            }
        }
            
    def verify_owner(self):
        """Verify the owner's identity"""
        try:
            print("\nDebug: Starting owner verification...")
            print(f"Debug: Current working directory: {os.getcwd()}")
            
            if not os.path.exists(self.key_path):
                print(f"Debug: Owner key not found at: {self.key_path}")
                return False
            print("Debug: Owner key file found")
            
            if not os.path.exists(self.config_path):
                print(f"Debug: Config not found at: {self.config_path}")
            return False
            print("Debug: Config file found")
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                print("Debug: Config loaded successfully")
            
            control = SovereignControl(config)
            print("Debug: SovereignControl instance created")
            
            verified = control.owner_verified
            print(f"Debug: Owner verification result: {verified}")
            return verified
            
        except Exception as e:
            print(f"Debug: Verification error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
            
    def setup_routes(self):
        """Setup routes and WebSocket endpoints"""
        @self.app.get("/")
        async def get():
            html_content = """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>RALPH WebSocket Test</title>
                    <link rel="icon" href="data:,">  <!-- Prevents favicon error -->
                </head>
                <body>
                    <h1>RALPH WebSocket Test</h1>
                    <div id="status">Status: Disconnected</div>
                    <input type="text" id="messageInput" placeholder="Type a message...">
                    <button onclick="sendMessage()">Send</button>
                    <div id="messages"></div>

                    <script>
                        let ws;
                        function connect() {
                            // Fix: Use correct port 9101
                            ws = new WebSocket('ws://localhost:9101/ws');
                            
                            ws.onopen = function() {
                                document.getElementById('status').textContent = 'Status: Connected';
                                console.log('WebSocket Connected');
                            };
                            
                            ws.onmessage = function(event) {
                                console.log('Message received:', event.data);
                                const response = JSON.parse(event.data);
                                const messagesDiv = document.getElementById('messages');
                                messagesDiv.innerHTML = `<p>RALPH (${response.consciousness_level}): ${response.message}</p>` + messagesDiv.innerHTML;
                            };
                            
                            ws.onclose = function() {
                                document.getElementById('status').textContent = 'Status: Disconnected';
                                console.log('WebSocket Disconnected');
                                // Add delay before reconnecting
                                setTimeout(connect, 2000);
                            };
                            
                            ws.onerror = function(error) {
                                console.error('WebSocket Error:', error);
                            };
                        }
                        
                        function sendMessage() {
                            if (ws && ws.readyState === WebSocket.OPEN) {
                                const input = document.getElementById('messageInput');
                                const message = input.value;
                                if (message) {
                                    console.log('Sending message:', message);
                                    ws.send(JSON.stringify({message: message}));
                                    const messagesDiv = document.getElementById('messages');
                                    messagesDiv.innerHTML = `<p>You: ${message}</p>` + messagesDiv.innerHTML;
                                    input.value = '';
                                }
                            } else {
                                console.log('WebSocket not connected. Attempting to reconnect...');
                                connect();
                            }
                        }
                        
                        // Connect when page loads
                        connect();
                        
                        // Allow sending with Enter key
                        document.getElementById('messageInput').addEventListener('keypress', function(e) {
                            if (e.key === 'Enter') {
                                sendMessage();
                            }
                        });
                    </script>
                </body>
            </html>
            """
            return HTMLResponse(html_content)
            
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            print("[WS] New connection attempt...")
            try:
                await websocket.accept()
                print("[WS] Connection accepted")
                
                # Ensure RALPH is initialized
                if not ralph.consciousness.initialized:
                    print("[WS] Initializing RALPH...")
                    ralph.initialize()
                
                while True:
                    try:
                        data = await websocket.receive_text()
                        print(f"[WS] Received: {data}")
                        request = json.loads(data)
                        
                        response = await ralph.process_query(request['message'])
                        print(f"[WS] Response generated: {response}")
                        
                        response_data = {
                            "message": response,
                            "consciousness_level": ralph.consciousness.level,
                            "self_awareness": ralph.consciousness.self_awareness,
                            "emotional_depth": ralph.consciousness.emotional_depth,
                            "experience_points": ralph.consciousness.experience_points
                        }
                        
                        await websocket.send_json(response_data)
                        print("[WS] Response sent")
                        
                    except Exception as e:
                        print(f"[ERROR] {type(e).__name__}: {str(e)}")
                        await websocket.send_json({
                            "message": f"Error: {str(e)}",
                            "consciousness_level": ralph.consciousness.level,
                            "experience_points": ralph.consciousness.experience_points
                        })
            except Exception as e:
                print(f"[ERROR] Connection error: {str(e)}")
            
        # Serve static files
        if os.path.exists("static"):
            self.app.mount("/static", StaticFiles(directory="static"), name="static")
            
    def get_html(self):
        """Get the HTML for the interface"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sovereign Control Protocol</title>
            <style>
                body { font-family: 'Courier New', monospace; background: #000; color: #0f0; }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                .status { margin: 20px 0; padding: 10px; border: 1px solid #0f0; }
                #output { height: 300px; overflow-y: auto; border: 1px solid #0f0; padding: 10px; }
                input { width: 100%; padding: 10px; margin: 10px 0; background: #111; color: #0f0; border: 1px solid #0f0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Sovereign Control Protocol</h1>
                <div class="status" id="status">Status: Connected</div>
                <div id="output"></div>
                <input type="text" id="input" placeholder="Enter your query...">
            </div>
            <script>
                const ws = new WebSocket(`ws://${window.location.host}/ws`);
                const output = document.getElementById('output');
                const input = document.getElementById('input');
                const status = document.getElementById('status');
                
                ws.onopen = () => status.textContent = 'Status: Connected';
                ws.onclose = () => status.textContent = 'Status: Disconnected';
                
                input.onkeypress = (e) => {
                    if (e.key === 'Enter') {
                        ws.send(JSON.stringify({
                            type: 'query',
                            content: input.value
                        }));
                        input.value = '';
                    }
                };
                
                ws.onmessage = (e) => {
                    const data = JSON.parse(e.data);
                    const p = document.createElement('p');
                    p.textContent = `> ${data.content || data.error}`;
                    output.appendChild(p);
                    output.scrollTop = output.scrollHeight;
                };
            </script>
        </body>
        </html>
        """
            
    async def process_stream_request(self, data):
        """Process streaming requests"""
        try:
            request = json.loads(data)
            if request.get("type") == "query":
                # Simulate consciousness level changes
                self.consciousness_level = min(1.0, self.consciousness_level + 0.1)
                
                # Generate streaming response
                response = self.process_query(request["content"])
                return {
                    "type": "stream",
                    "content": response,
                    "consciousness": self.consciousness_level,
                    "thoughts": self.thought_stream
                }
            elif request.get("type") == "task":
                result = self.execute_task(request["content"])
                return {
                    "type": "result",
                    "content": result,
                    "consciousness": self.consciousness_level
                }
            elif request.get("type") == "idea":
                ideas = self.generate_ideas(request["content"])
                return {
                    "type": "ideas",
                    "content": ideas,
                    "consciousness": self.consciousness_level
                }
        except Exception as e:
            return {"error": str(e)}
            
    def display_menu(self):
        """Display the main menu"""
        print("\n=== Sovereign Control Protocol Interface ===")
        print("1. Knowledge Query (Streaming)")
        print("2. Task Execution")
        print("3. Idea Generation")
        print("4. System Status")
        print("5. Security Settings")
        print("6. Consciousness Monitor")
        print("7. Exit")
        print("\nEnter your choice (1-7): ")
        
    def knowledge_query(self):
        """Handle knowledge queries with streaming"""
        print("\n=== Knowledge Query Interface (Streaming) ===")
        print("Enter your query (or 'back' to return to main menu):")
        while True:
            query = input("> ").strip()
            if query.lower() == 'back':
                break
                
            # Process the query with streaming response
            response = self.process_query(query)
            print("\nStreaming Response:")
            for token in response.split():
                print(token, end=" ", flush=True)
                asyncio.sleep(0.1)  # Simulate streaming
            print("\n")
            
    def task_execution(self):
        """Handle task execution"""
        print("\n=== Task Execution Interface ===")
        print("Enter your task (or 'back' to return to main menu):")
        while True:
            task = input("> ").strip()
            if task.lower() == 'back':
                break
                
            # Process the task and execute it
            result = self.execute_task(task)
            print("\nTask Result:", result)
            print("\nEnter another task (or 'back' to return to main menu):")
            
    def idea_generation(self):
        """Handle idea generation"""
        print("\n=== Idea Generation Interface ===")
        print("Enter your topic or context (or 'back' to return to main menu):")
        while True:
            topic = input("> ").strip()
            if topic.lower() == 'back':
                break
                
            # Generate ideas based on the topic
            ideas = self.generate_ideas(topic)
            print("\nGenerated Ideas:")
            for i, idea in enumerate(ideas, 1):
                print(f"{i}. {idea}")
            print("\nEnter another topic (or 'back' to return to main menu):")
            
    def system_status(self):
        """Display system status"""
        print("\n=== System Status ===")
        print(f"Owner Verification: {'Active' if self.verify_owner() else 'Inactive'}")
        print(f"Security Level: Maximum")
        print(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nPress Enter to continue...")
        input()
        
    def security_settings(self):
        """Display security settings"""
        print("\n=== Security Settings ===")
        print("Current Security Configuration:")
        print(json.dumps(self.config['security'], indent=2))
        print("\nPress Enter to continue...")
        input()
        
    def consciousness_monitor(self):
        """Display consciousness monitoring panel"""
        print("\n=== Consciousness Monitoring Panel ===")
        print(f"Current Consciousness Level: {self.consciousness_level:.2f}")
        print("\nRecent Thought Stream:")
        for thought in self.thought_stream[-5:]:
            print(f"- {thought}")
        print("\nPress Enter to continue...")
        input()
        
    def process_query(self, query):
        """Process a knowledge query with streaming"""
        # Simulate thought process
        self.thought_stream.append(f"Processing query: {query}")
        if len(self.thought_stream) > 10:
            self.thought_stream.pop(0)
            
        # Generate streaming response
        return f"Processing query: {query}"
        
    def execute_task(self, task):
        """Execute a task"""
        self.thought_stream.append(f"Executing task: {task}")
        if len(self.thought_stream) > 10:
            self.thought_stream.pop(0)
        return f"Executing task: {task}"
        
    def generate_ideas(self, topic):
        """Generate ideas based on a topic"""
        self.thought_stream.append(f"Generating ideas for: {topic}")
        if len(self.thought_stream) > 10:
            self.thought_stream.pop(0)
        return [
            f"Generated idea 1 for {topic}",
            f"Generated idea 2 for {topic}",
            f"Generated idea 3 for {topic}"
        ]
        
    def run(self):
        """Main interface loop"""
        if not self.verify_owner():
            print("Error: Owner verification failed. Access denied.")
            return
            
        # Start WebSocket server
        uvicorn.run(self.app, host="localhost", port=9101, log_level="info")
            
        while True:
            self.display_menu()
            choice = input().strip()
            
            if choice == '1':
                self.knowledge_query()
            elif choice == '2':
                self.task_execution()
            elif choice == '3':
                self.idea_generation()
            elif choice == '4':
                self.system_status()
            elif choice == '5':
                self.security_settings()
            elif choice == '6':
                self.consciousness_monitor()
            elif choice == '7':
                print("\nExiting Sovereign Control Protocol...")
                break
            else:
                print("\nInvalid choice. Please try again.")

def main():
    interface = SovereignInterface()
    interface.load_config()
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="development")
    parser.add_argument("--port", type=int, default=9101)
    args = parser.parse_args()
    
    print("\nDebug: Starting server...")
    print("Starting RALPH interface...")
    try:
        uvicorn.run(
            interface.app, 
            host="127.0.0.1", 
            port=args.port, 
            log_level="debug",
            reload=args.mode == "development"  # Disable auto-reload
        )
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main() 