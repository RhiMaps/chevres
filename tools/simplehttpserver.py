
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys
import os


class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    script_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.abspath(os.path.join(script_path, os.pardir))
    os.chdir(root_path)


    test(CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
