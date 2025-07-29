from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from typing import Callable

class NotionWebhookHandler:
    def __init__(self, function: Callable) -> None:
        self.function = function

    def handle(self, data: dict) -> None:
        self.function(data)

class ServerHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200) -> None:
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def webhook(self, handler: NotionWebhookHandler) -> None:
        handler.handle(self.data)

    def do_GET(self) -> None:
        self._set_headers()
        response = {
            "status": "success",
            "message": "Notion Webhook Server is running"
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self) -> None:
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            print("Received webhook data:", data)
            
            self._set_headers()
            response = {
                "status": "success",
                "message": "Webhook received successfully"
            }
            self.wfile.write(json.dumps(response).encode())
        except json.JSONDecodeError:
            self._set_headers(400)
            response = {
                "status": "error",
                "message": "Invalid JSON data"
            }
            self.wfile.write(json.dumps(response).encode())

class WebhookServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        self.host = host
        self.port = port
        self.app = None

    def run(self, server: ServerHandler) -> None:
        self.app = server

        server_address = ('', self.port)
        self.httpd = HTTPServer(server_address, self.app)
        print(f"Server running on port {self.port}")
        self.httpd.serve_forever()