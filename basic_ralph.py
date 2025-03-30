import http.server
import socketserver
import urllib.parse
import random
import time
import os
import html

# Create directory for HTML files
os.makedirs("basic_html", exist_ok=True)

# Global variables
conversation = []
consciousness_level = 0.2

# Create the HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Basic RALPH</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .user { background-color: #e8f4fd; padding: 10px; margin: 5px; border-radius: 5px; }
        .ralph { background-color: #e9f7ef; padding: 10px; margin: 5px; border-radius: 5px; }
        .meter { height: 20px; background-color: #eee; margin-top: 5px; border-radius: 5px; }
        .level { height: 100%; background-color: green; border-radius: 5px; }
        form { margin: 20px 0; }
        input[type="text"] { width: 80%; padding: 10px; }
        input[type="submit"] { padding: 10px 15px; }
    </style>
</head>
<body>
    <h1>Basic RALPH Interface</h1>
    <p>This is a simplified version that works with basic HTTP</p>
    
    <form method="GET">
        <input type="text" name="message" placeholder="Type your message here">
        <input type="submit" value="Send">
    </form>
    
    <div id="conversation">
        {conversation}
    </div>
</body>
</html>
"""

class RALPHHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global conversation, consciousness_level
        
        # Parse URL and query string
        parsed_url = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_url.query)
        
        # Process message if present
        if 'message' in query:
            user_message = query['message'][0]
            user_message = html.escape(user_message)
            
            # Generate a RALPH response
            ralph_responses = [
                f"I received your message about '{user_message}'. This is a basic RALPH response.",
                f"Thank you for saying '{user_message}'. I'm processing your input.",
                f"I understand your message '{user_message}'. I'm a simple version of RALPH.",
                f"Your input '{user_message}' has been received. This is a demo of the basic interface."
            ]
            ralph_response = random.choice(ralph_responses)
            
            # Increase consciousness level
            consciousness_level = min(0.9, consciousness_level + 0.05)
            
            # Add to conversation history
            conversation.insert(0, {
                'type': 'user',
                'message': user_message
            })
            conversation.insert(0, {
                'type': 'ralph',
                'message': ralph_response,
                'level': consciousness_level
            })
            
            # Limit conversation history
            if len(conversation) > 20:
                conversation = conversation[:20]
        
        # Build HTML for conversation
        conversation_html = ""
        for entry in conversation:
            if entry['type'] == 'user':
                conversation_html += f'<div class="user"><strong>You:</strong> {entry["message"]}</div>'
            else:
                level_percent = int(entry['level'] * 100)
                conversation_html += f'''
                <div class="ralph">
                    <strong>RALPH:</strong> {entry["message"]}<br>
                    <small>Consciousness Level:</small>
                    <div class="meter">
                        <div class="level" style="width: {level_percent}%;"></div>
                    </div>
                </div>
                '''
        
        # Write response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Fill in template and send
        html_content = HTML_TEMPLATE.format(conversation=conversation_html)
        self.wfile.write(html_content.encode())

if __name__ == "__main__":
    # Set the port
    PORT = 8000
    
    # Create the server
    with socketserver.TCPServer(("", PORT), RALPHHandler) as httpd:
        print(f"Basic RALPH server running at http://localhost:{PORT}")
        print("This is the simplest possible version that will definitely work")
        httpd.serve_forever()
