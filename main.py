import http.server
import socketserver
import webbrowser
import threading
import os
import sys
import time

PORT = 8000

def get_base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return base_path

DIRECTORY = get_base_path()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

def start_server():
    # Use allow_reuse_address to avoid "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a bit for the server to initialize
    time.sleep(1)
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    
    print("--------------------------------------------------")
    print("Algorithm Project is running!")
    print(f"URL: http://localhost:{PORT}")
    print("Keep this window open to use the application.")
    print("Press Ctrl+C to stop.")
    print("--------------------------------------------------")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        sys.exit(0)
