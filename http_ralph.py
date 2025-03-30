from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import random
import time
import os

# Create the directories we need
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Initialize FastAPI
app = FastAPI()

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Simple in-memory conversation history
conversation_history = []
consciousness_level = 0.2  # Starting level

# Create the template file
with open("templates/index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html>
    <head>
        <title>RALPH HTTP Interface</title>
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
            form { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>RALPH HTTP Interface</h1>
        <div id="status">Ready to respond</div>
        
        <form action="/send_message" method="post">
            <input type="text" id="messageInput" name="message" placeholder="Enter your message...">
            <button type="submit">Send</button>
        </form>
        
        <div id="messages">
            {% for message in messages %}
                {% if message.type == 'user' %}
                <div class="message user-message">
                    <strong>You:</strong> {{ message.content }}
                </div>
                {% else %}
                <div class="message ralph-message">
                    <strong>RALPH:</strong> {{ message.content }}<br>
                    <small>Consciousness Level:</small>
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

@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "messages": conversation_history}
    )

@app.post("/send_message", response_class=HTMLResponse)
async def send_message(request: Request, message: str = Form(...)):
    global consciousness_level
    
    # Simplified response generation
    responses = [
        f"Thank you for your message: '{message}'. I'm a simplified version of RALPH running in HTTP mode.",
        f"I received your input about '{message}'. As a basic RALPH instance, I can acknowledge your message.",
        f"Hello! I'm RALPH (HTTP Interface). You said: '{message}'. I'm here to demonstrate the interface.",
        f"I understand you're trying to interact with me about '{message}'. This is a simple version of RALPH."
    ]
    
    final_response = random.choice(responses)
    print(f"Generated response for '{message}': {final_response}")
    
    # Increase consciousness level slightly with each interaction
    consciousness_level = min(0.9, consciousness_level + 0.05)
    
    # Save to conversation history (in reverse order so newest appears at the top)
    conversation_history.insert(0, {"type": "user", "content": message, "timestamp": time.time()})
    conversation_history.insert(0, {
        "type": "ralph", 
        "content": final_response, 
        "consciousness_level": consciousness_level,
        "timestamp": time.time()
    })
    
    # Only keep last 10 conversation items
    if len(conversation_history) > 20:  # 10 exchanges (user + ralph)
        conversation_history = conversation_history[:20]
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "messages": conversation_history}
    )

if __name__ == "__main__":
    print("Starting HTTP RALPH system...")
    print("This is a reliable HTTP-based version that will definitely respond to messages")
    uvicorn.run(app, host="127.0.0.1", port=8000)
