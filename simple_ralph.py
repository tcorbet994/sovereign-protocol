from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn
import json
import random
import time

# Initialize FastAPI
app = FastAPI()

# Simple in-memory conversation history
conversation_history = []
consciousness_level = 0.2  # Starting level

@app.get("/")
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>RALPH Simple Interface</title>
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
        <h1>RALPH Simple Interface</h1>
        <div id="status">Connected to RALPH</div>
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
    global consciousness_level
    await websocket.accept()
    print("WebSocket connection established")
    
    while True:
        try:
            # Receive message
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            request = json.loads(data)
            message = request['message']
            
            print(f"Processing message: {message}")
            
            # Simplified response generation
            responses = [
                f"Thank you for your message: '{message}'. I'm a simplified version of RALPH running in demonstration mode.",
                f"I received your input about '{message}'. As a basic RALPH instance, I can acknowledge your message.",
                f"Hello! I'm RALPH (Simplified). You said: '{message}'. I'm here to demonstrate the interface.",
                f"I understand you're trying to interact with me about '{message}'. This is a basic version of RALPH."
            ]
            
            final_response = random.choice(responses)
            print(f"Generated response: {final_response}")
            
            # Increase consciousness level slightly with each interaction
            consciousness_level = min(0.9, consciousness_level + 0.05)
            
            # Save to conversation history
            conversation_history.append({
                "user": message,
                "ralph": final_response,
                "timestamp": time.time()
            })
            
            # Only keep last 10 conversations
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            # Send response
            print("Sending response back to client...")
            await websocket.send_json({
                "message": final_response,
                "consciousness_level": f"{consciousness_level:.2f}"
            })
            print("Response sent successfully")
            
        except Exception as e:
            print(f"Error in websocket loop: {e}")
            try:
                await websocket.send_json({
                    "message": f"Error processing request: {str(e)}",
                    "consciousness_level": "0.00"
                })
                print("Error response sent")
            except Exception as se:
                print(f"Failed to send error response: {se}")

if __name__ == "__main__":
    print("Starting Simple RALPH system...")
    print("This is a simplified version that will definitely respond to messages")
    uvicorn.run(app, host="127.0.0.1", port=8000)
