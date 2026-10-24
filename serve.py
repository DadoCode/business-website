"""Local preview server with clean URLs (/about -> about.html), matching the static hosts.

Usage: python3 serve.py [port]
"""
import http.server, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path != "/" and "." not in os.path.basename(path) and os.path.isfile(os.path.join(ROOT, path.lstrip("/") + ".html")):
            self.path = path + ".html"
        elif not os.path.exists(os.path.join(ROOT, path.lstrip("/"))):
            self.path = "/404.html"
        return super().send_head()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Serving on http://localhost:{port}")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
