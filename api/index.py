from http.server import BaseHTTPRequestHandler
import json
import traceback
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            json.dumps({"status": "ok", "message": "GET works"}, ensure_ascii=False).encode("utf-8")
        )

    def do_POST(self):
        
        print("POST handler reached - openai chat test v1")

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"

            print("RAW BODY:", raw_body)

            data = json.loads(raw_body) if raw_body else {}
            issue = data.get("issue", "").strip()

            if not issue:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(
                    json.dumps({
                        "status": "error",
                        "version": "openai-chat-test-v1",
                        "error": "issue is required"
                    }, ensure_ascii=False).encode("utf-8")
                )
                return

            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL")

            from openai import OpenAI

            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )

            completion = client.chat.completions.create(
                model="gpt-5.4",
                messages=[
                    {"role": "system", "content": "사용자의 이슈를 한두 문장으로 간단히 요약해 주세요."},
                    {"role": "user", "content": issue}
                ]
            )

            answer = completion.choices[0].message.content
            
            response = {
                "status": "ok",
                "version": "openai-chat-test-v1",
                "issue": issue,
                "answer": answer
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
                json.dumps({
                    "status": "error",
                    "version": "openai-chat-test-v1",
                    "error": str(e)
                }, ensure_ascii=False).encode("utf-8"))