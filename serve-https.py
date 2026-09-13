#!/usr/bin/env python3
"""Local HTTPS server for Quest WebXR testing."""
import http.server
import ssl
import sys

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8443
CERT = ".certs/dev.pem"
KEY = ".certs/dev-key.pem"

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header(
            "Permissions-Policy",
            "xr-spatial-tracking=(self), accelerometer=(self), gyroscope=(self)",
        )
        self.send_header(
            "Feature-Policy",
            "xr-spatial-tracking 'self'; accelerometer 'self'; gyroscope 'self'",
        )
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

httpd = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(CERT, KEY)
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
print("HTTPS https://127.0.0.1:%s/" % PORT)
print("Quest  https://192.168.1.76:%s/" % PORT)
print("Accept the certificate warning on the headset, then tap Enter VR.")
httpd.serve_forever()
