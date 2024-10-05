import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

public_path = Path(__file__).resolve().parent.parent / "public"
PREFIX = "/tripos-notes/"

class MyHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        global public_path, PREFIX
        if path.startswith(PREFIX):
            path = path[len(PREFIX):]
        elif path.startswith("/"):
            path = path[1:]

        return os.path.join(public_path, path)

PORT = 8000

httpd = HTTPServer(("", PORT), MyHandler)
print(f"Serving on localhost:{PORT}")
httpd.serve_forever()
