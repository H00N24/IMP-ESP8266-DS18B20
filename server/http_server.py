"""File with HTTP server function

Author:
    Ondrej Kurak
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Request_Handler(BaseHTTPRequestHandler):
    """Simple HTTP request hadler
    """

    def do_GET(self):
        """HTTP GET

        Sends main page for every unknown url.
        """
        self.path = self.path.replace('..', '/')
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        main_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(main_dir + self.path) as inp:
                text = inp.read()
        except:
            with open(main_dir + '/index.html') as inp:
                text = inp.read()

        self.wfile.write(bytes(text, "utf8"))


def run_http_server():
    """HTTP server
    """
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, Request_Handler)
    print('HTTP server: OK')
    httpd.serve_forever()
