from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. OpenAI 클라이언트 초기화 (환경변수 사용)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

print("OPENAI_API_KEY exists:", bool(api_key))
print("OPENAI_API_KEY prefix:", api_key[:10] if api_key else None)
print("OPENAI_BASE_URL:", base_url)

if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

client = OpenAI(api_key=api_key)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 2. 요청 데이터 읽기
        content_length = int(self.headers('Content-Length', 0))
        if content_length == 0:
            self.send_response(400)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "error",
                "message": "요청 본문이 비어 있습니다."
            }, ensure_ascii=False).encode('utf-8'))
            return
        
        
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            user_issue = data.get("issue", "발생한 품질 문제에 대한 설명이 없습니다.")
            data = json.loads(post_data.decode("utf-8"))
            user_issue = data.get("issue", "").strip()

            if not user_issue:
                self.send_response(400)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "error",
                    "message": "'issue' 값을 입력해주세요."
                }, ensure_ascii=False).encode('utf-8'))
                return

            # 3. OpenAI API 호출 (8D 리포트 생성 로직)
            # 모델명 수정 가능
            response = client.chat.completions.create(
                model="gpt-5.4", 
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "당신은 글로벌 제조 기업의 품질 관리 전문가입니다. "
                            "사용자의 입력 내용을 바탕으로 표준 8D 리포트(D1~D8) 초안을 작성하세요. "
                            "전문 용어를 사용하고, 각 단계별로 구체적인 예시를 포함하여 한국어로 작성해 주세요."
                        )
                    },
                    {"role": "user", "content": f"다음 품질 문제에 대한 8D 리포트를 작성해줘: {user_issue}"}
                ],
                temperature=0.7
            )

            # 4. 성공 응답 전송
            result = response.choices[0].message.content
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            # CORS 설정 (프론트엔드 연동 대비)
            self.send_header('Access-Control-Allow-Origin', '*') 
            self.end_headers()
            
            response_body = {
                "status": "success",
                "data": {
                    "issue": user_issue,
                    "report": result
                }
            }
            self.wfile.write(json.dumps(response_body, ensure_ascii=False).encode('utf-8'))

        except Exception as e:
            # 에러 발생 시 처리
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            print(f"8D generation error: {e}")
            error_message = {
                "status": "error",
                "message": "8D 리포트 생성 중 오류가 발생했습니다."
            }
            self.wfile.write(json.dumps(error_message, ensure_ascii=False).encode('utf-8'))

    def do_GET(self):
        # API 상태 확인용 GET 핸들러
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "success",
            "message": "Auto8D API is running. Please use POST method with 'issue' data."
        }, ensure_ascii=False).encode('utf-8'))


    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()