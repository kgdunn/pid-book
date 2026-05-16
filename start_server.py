import http.server
import os
import pathlib
import socketserver

PORT = 8080


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        "": "text/html",  # extensionless pages served as HTML
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
        # Pagefind shard types — served as binary; browser fetches them raw
        ".pf_index": "application/octet-stream",
        ".pf_fragment": "application/octet-stream",
        ".pf_meta": "application/octet-stream",
        ".pagefind": "application/octet-stream",
    }

    def log_message(self, format, *args):
        pass  # silence per-request noise; uncomment to debug


# ThreadingTCPServer handles each request in its own thread, so Pagefind's
# 10+ concurrent shard fetches don't queue behind each other.
class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


web_dir = pathlib.Path(".") / "_build" / "html"
os.chdir(web_dir)
httpd = ThreadedServer(("localhost", PORT), HttpRequestHandler)

try:
    print(f"http://localhost:{PORT}")
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
