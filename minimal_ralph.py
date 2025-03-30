from http.server import BaseHTTPRequestHandler, HTTPServer

class MinimalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Minimal RALPH</h1>
            <p>This is working!</p>
            <form>
                <input type="text" name="message">
                <input type="submit" value="Send">
            </form>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 8000), MinimalHandler)
    print("Minimal RALPH server started at http://127.0.0.1:8000")
    server.serve_forever()
