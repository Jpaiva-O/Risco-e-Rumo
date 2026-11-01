import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-uptime.sh"
SITE_HTML = b"<!doctype html><html><head><title>Risco &amp; Rumo</title></head></html>"


class SiteHandler(BaseHTTPRequestHandler):
    routes = {}
    requests = []

    def do_GET(self):
        self.requests.append(self.path)
        status, body = self.routes.get(self.path, (404, b"Not found"))
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


class UptimeCheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), SiteHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()
        cls.server.server_close()

    def setUp(self):
        SiteHandler.routes = {"/": (200, SITE_HTML), "/index-7.html": (200, SITE_HTML)}
        SiteHandler.requests = []

    def run_check(self):
        env = os.environ.copy()
        env["SITE_URL"] = f"http://127.0.0.1:{self.server.server_port}"
        env["UPTIME_RETRIES"] = "0"
        return subprocess.run(
            ["bash", str(SCRIPT)], cwd=ROOT, env=env, text=True, capture_output=True, timeout=10
        )

    def test_checks_both_healthy_routes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(SiteHandler.requests, ["/", "/index-7.html"])

    def test_missing_legacy_route_fails(self):
        del SiteHandler.routes["/index-7.html"]
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("index-7.html", result.stderr)

    def test_wrong_page_with_200_status_fails(self):
        SiteHandler.routes["/"] = (200, b"<html><title>Another site</title></html>")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("without the expected site HTML", result.stderr)
        self.assertEqual(SiteHandler.requests, ["/"])

    def test_brand_in_non_html_response_fails(self):
        SiteHandler.routes["/"] = (200, b"Risco &amp; Rumo")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("without the expected site HTML", result.stderr)


if __name__ == "__main__":
    unittest.main()
