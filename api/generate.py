# Vercel 서버리스 함수가 작동하는지 확인하는 기초 코드
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    # GET 요청이 들어왔을 때 (브라우저에서 주소로 접속했을 때)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # 응답 데이터
        response_data = {
            "status": "success",
            "message": "Auto8D API is ready! Please use POST method to generate reports."
        }
        
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return

    # POST 요청이 들어왔을 때 (나중에 프론트엔드에서 데이터를 보낼 때)
    def do_POST(self):
        # 나중에 여기에 AI 로직이 들어갑니다.
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "POST request received"}).encode('utf-8'))
        return