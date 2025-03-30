import http.server
import socketserver
import urllib.parse
import random
import html

# Global variables
conversation = []
consciousness_level = 0.2

# Very simple HTML template with no complex formatting
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Ultra Basic RALPH</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
    </style>
</head>
<body>
    <h1>Ultra Basic RALPH</h1>
    <p>This is the simplest possible version</p>
    
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
            conversation.insert(0, f"<p><strong>You:</strong> {user_message}</p>")
            conversation.insert(0, f"<p><strong>RALPH:</strong> {ralph_response}</p>")
            
            # Limit conversation history
            if len(conversation) > 20:
                conversation = conversation[:20]
        
        # Build HTML for conversation
        conversation_html = "\n".join(conversation)
        
        # Write response
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Fill in template and send
        html_content = HTML.replace("{conversation}", conversation_html)
        self.wfile.write(html_content.encode())

if __name__ == "__main__":
    # Set the port
    PORT = 8000
    
    # Create the server
    with socketserver.TCPServer(("", PORT), RALPHHandler) as httpd:
        print(f"Ultra Basic RALPH server running at http://localhost:{PORT}")
        print("This is the absolutely simplest version that will definitely work")
        httpd.serve_forever()
