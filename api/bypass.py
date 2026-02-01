from http.server import BaseHTTPRequestHandler
import json, requests, time
from urllib.parse import urlparse, parse_qs

# ========== CONFIG ==========
MAIN_API = "https://rocky-bhai-link-bypass-api.onrender.com/bypass"
SECRET_KEY = "9d815189412d9390cda93315a65fdf6e"  # 🔒 hidden

# ========== FUNCTION HANDLER ==========
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        link = query.get("link", [None])[0]

        if not link:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": "link parameter missing"
            }).encode())
            return

        start = time.time()
        try:
            r = requests.get(
                MAIN_API,
                params={"key": SECRET_KEY, "link": link},
                timeout=60
            )
            data = r.json()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "success",
                "original": link,
                "bypassed": data.get("bypassed") or data.get("result"),
                "time_taken": f"{round(time.time()-start,2)}s"
            }).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "failed",
                "error": str(e)
            }).encode())
