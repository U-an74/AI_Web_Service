#백엔드
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
        
        print("POST handler reached - 8d draft v1")

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
                        "version": "8d-draft-v1",
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
                    {
                        "role": "system",
                        "content": (
                            "당신은 품질관리 8D 리포트 작성 도우미입니다. "
                            "사용자가 입력한 문제를 바탕으로 8D 초안을 한국어로 작성하세요. "
                            "출력은 반드시 아래 형식을 따르세요.\n\n"
                            "D1. 대응팀 구성: ...\n"
                            "D2. 문제 정의: ...\n"
                            "D3. 임시 조치: ...\n"
                            "D4. 근본 원인 분석: ...\n"
                            "D5. 영구 대책 선정: ...\n"
                            "D6. 대책 실행 및 검증: ...\n"
                            "D7. 재발 방지: ...\n"
                            "D8. 종료 및 공유: ...\n\n"
                            "각 항목은 1~2문장 정도로 간결하고 실무적으로 작성하세요."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"문제: {issue}"
                    }
                ]
            )

            report_text = completion.choices[0].message.content
            
            response = {
                "status": "ok",
                "version": "8d-draft-v1",
                "issue": issue,
                "report_text": report_text
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
                    "version": "8d-draft-v1",
                    "error": str(e)
                }, ensure_ascii=False).encode("utf-8")
            )