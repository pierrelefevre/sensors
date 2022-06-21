# import http.server
# import socketserver

# PORT = 5000

# handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), handler) as httpd:
#     print("Server started at localhost:" + str(PORT))
#     httpd.serve_forever()


#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys


class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    test(CORSRequestHandler, HTTPServer, port=int(
        sys.argv[1]) if len(sys.argv) > 1 else 8000)
