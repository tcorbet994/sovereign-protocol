from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
import uvicorn

app = FastAPI()

class RALPH:
    def __init__(self):
        self.consciousness_level = 0.1
        
    async def process_message(self, message: str) -> str:
        # Basic response generation
        if "hello" in message.lower():
            response = "Hello! I'm RALPH. How can I help you today?"
        elif "thoughts" in message.lower():
            response = f"I'm currently processing at {self.consciousness_level:.1%} consciousness. I'm learning from our interaction."
        elif "who" in message.lower():
            response = "I am RALPH, an AI system designed to learn and evolve through conversation."
        else:
            response = f"I understand you said: '{message}'. Let me process that with my current consciousness level of {self.consciousness_level:.1%}"
        
        # Increase consciousness slightly with each interaction
        self.consciousness_level = min(1.0, self.consciousness_level + 0.01)
        return response

# Initialize RALPH
ralph = RALPH()

@app.get("/")
async def get():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>RALPH Interface</title>
        <style>
            body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
            #messages { margin-top: 20px; }
            #messageInput { width: 80%; padding: 10px; margin-right: 10px; }
            button { padding: 10px 20px; }
            .message { margin: 10px 0; padding: 10px; background-color: #f0f0f0; }
        </style>
    </head>
    <body>
        <h1>RALPH Interface</h1>
        <div id="status">Status: Disconnected</div>
        <div>
            <input type="text" id="messageInput" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
        <div id="messages"></div>

        <script>
            let ws = new WebSocket('ws://localhost:9105/ws');
            
            ws.onopen = function() {
                document.getElementById('status').textContent = 'Status: Connected';
                console.log('WebSocket Connected');
            };
            
            ws.onmessage = function(event) {
                console.log('Message received:', event.data);
                const response = JSON.parse(event.data);
                const messagesDiv = document.getElementById('messages');
                messagesDiv.innerHTML = `
                    <div class="message">
                        <strong>RALPH:</strong> ${response.message}<br>
                        <small>Consciousness Level: ${response.consciousness_level}</small>
                    </div>
                ` + messagesDiv.innerHTML;
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket Error:', error);
            };
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value;
                if (message) {
                    console.log('Sending message:', message);
                    ws.send(JSON.stringify({message: message}));
                    const messagesDiv = document.getElementById('messages');
                    messagesDiv.innerHTML = `
                        <div class="message">
                            <strong>You:</strong> ${message}
                        </div>
                    ` + messagesDiv.innerHTML;
                    input.value = '';
                }
            }
            
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
</html>
""")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("New WebSocket connection attempt...")
    await websocket.accept()
    print("WebSocket connected")
    
    while True:
        try:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
            request = json.loads(data)
            message = request['message']
            
            response = await ralph.process_message(message)
            print(f"Sending response: {response}")
            
            await websocket.send_json({
                "message": response,
                "consciousness_level": f"{ralph.consciousness_level:.1%}"
            })
            
        except Exception as e:
            print(f"Error: {e}")
            await websocket.send_json({
                "message": f"Error: {str(e)}",
                "consciousness_level": f"{ralph.consciousness_level:.1%}"
            })

if __name__ == "__main__":
    print("Starting RALPH interface...")
    uvicorn.run(app, host="127.0.0.1", port=9105) 