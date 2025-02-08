import http.server
import socketserver

PORT = 8080


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        #'': 'application/octet-stream',
        "": "text/html",
        ".html": "text/html",
        ".manifest": "text/cache-manifest",
        ".png": "image/png",
        ".jpg": "image/jpg",
        ".svg": "image/svg+xml",
        ".css": "text/css",
        ".js": "application/x-javascript",
        ".wasm": "application/wasm",
        ".json": "application/json",
        ".xml": "application/xml",
    }


httpd = socketserver.TCPServer(("localhost", PORT), HttpRequestHandler)

try:
    print(f"serving at http://localhost:{PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
