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
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

class SovereignInterface:
    def __init__(self):
        self.config_path = Path("config/default_config.json")
        self.key_path = Path("security/biometric/sovereign.key")
        self.owner_key_path = Path("security/biometric/owner_key.bin")
        self.load_config()
        self.consciousness_level = 0.0
        self.thought_stream = []
        self.app = FastAPI()
        self.setup_websocket()
        
    def load_config(self):
        """Load the configuration file"""
        if not self.config_path.exists():
            print("Error: Configuration file not found. Please run initialization first.")
            sys.exit(1)
            
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
            
    def verify_owner(self):
        """Verify the owner's identity"""
        if not self.key_path.exists() or not self.owner_key_path.exists():
            print("Error: Owner verification files not found. Please run initialization first.")
            return False
            
        try:
            # Read the stored keys
            with open(self.key_path, 'rb') as f:
                stored_data = f.read()
                salt = stored_data[:16]
                encrypted_key = stored_data[16:]
                
            with open(self.owner_key_path, 'rb') as f:
                owner_data = f.read()
                owner_salt = owner_data[:16]
                owner_key = owner_data[16:]
                
            # Verify the keys match
            return encrypted_key == owner_key
        except Exception as e:
            print(f"Error during owner verification: {str(e)}")
            return False
            
    def setup_websocket(self):
        """Setup WebSocket endpoints"""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            
            if not self.verify_owner():
                await websocket.send_json({"error": "Owner verification failed"})
                return
                
            try:
                while True:
                    data = await websocket.receive_text()
                    response = await self.process_stream_request(data)
                    await websocket.send_json(response)
            except Exception as e:
                print(f"WebSocket error: {str(e)}")
                
        # Serve static files
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
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
        uvicorn.run(self.app, host="localhost", port=8000)
            
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

if __name__ == "__main__":
    interface = SovereignInterface()
    interface.run() 