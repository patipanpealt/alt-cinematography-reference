#!/usr/bin/env python3
"""Static server for the site. chdir's explicitly — os.getcwd() is not readable
from the launcher's default working directory on this external volume."""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site")
os.chdir(ROOT)

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4173

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))

httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
print(f"serving {ROOT} at http://localhost:{PORT}", flush=True)
httpd.serve_forever()
