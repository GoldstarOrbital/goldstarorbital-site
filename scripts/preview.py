"""Local preview of Pages clean URLs; deployment headers are verified live."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import os

os.chdir(Path(__file__).resolve().parents[1])
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        if path != '/' and not Path('.'+path).exists() and Path('.'+path+'.html').is_file():
            self.path=path+'.html'
        return super().do_GET()
ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
