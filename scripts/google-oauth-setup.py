#!/usr/bin/env python3
"""
Google OAuth 2.0 — получение refresh token для Jarvis.
Используется один раз для авторизации.
"""

import http.server
import urllib.parse
import webbrowser
import json
import threading
import time
import urllib.request

CLIENT_ID = "140943545360-2chcflqvnco1pg44ipbpf32ftk1ub232.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8090/callback"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
]

auth_code = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Authorization successful! You can close this window.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logs

def main():
    global auth_code
    
    # Build auth URL
    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join(SCOPES),
            "access_type": "offline",
            "prompt": "consent",
        })
    )
    
    print(f"\nОткрываю браузер для авторизации...")
    print(f"Если браузер не открылся, перейди по ссылке:\n{auth_url}\n")
    
    # Start local server
    server = http.server.HTTPServer(('localhost', 8090), Handler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()
    
    webbrowser.open(auth_url)
    
    # Wait for callback
    print("Жду авторизации...")
    for _ in range(120):  # Wait up to 2 minutes
        if auth_code:
            break
        time.sleep(1)
    
    if not auth_code:
        print("Timeout! Не удалось получить код авторизации.")
        return
    
    print(f"Получен код авторизации!")
    
    # Exchange code for tokens
    token_data = urllib.parse.urlencode({
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }).encode()
    
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    
    try:
        resp = urllib.request.urlopen(req)
        tokens = json.loads(resp.read().decode())
        
        print(f"\n{'='*50}")
        print(f"REFRESH TOKEN:")
        print(tokens.get("refresh_token", "NOT FOUND"))
        print(f"{'='*50}")
        
        # Save to file
        config = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": tokens.get("refresh_token"),
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        with open("/root/.openclaw/workspace/google-oauth.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"\nСохранено в /root/.openclaw/workspace/google-oauth.json")
        print(f"Готово!")
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
