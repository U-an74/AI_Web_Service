from http.server import BaseHTTPRequestHandler
import json
import traceback
import os

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

print("STEP 1: env check")
print("OPENAI_API_KEY exists:", bool(api_key))
print("OPENAI_BASE_URL:", base_url)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            json.dumps({"status": "ok", "message": "GET works"}, ensure_ascii=False).encode("utf-8")
        )

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

            print("RAW BODY:", raw_body)

            data = json.loads(raw_body) if raw_body else {}
            issue = data.get("issue", "")

            response = {
                "status": "ok",
                "received_issue": issue
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            print("ERROR:", repr(e))
            traceback.print_exc()

            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False).encode("utf-8")
            )