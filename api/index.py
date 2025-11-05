from http.server import BaseHTTPRequestHandler
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Получаем параметры хоста
        host = os.getenv('HOST', 'localhost')
        port = os.getenv('PORT', '8000')
        debug = os.getenv('DEBUG', 'False')
        
        # Получаем параметры подключения к БД
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'test_db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        db_url = os.getenv('DB_URL', '')
        
        # Формируем HTML страницу
        db_password_display = '*' * len(db_password) if db_password else 'Not set'
        db_url_display = db_url if db_url else 'Not set'
        
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Configuration</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }}
        h1 {{
            color: #667eea;
            font-size: 3em;
            text-align: center;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }}
        .section-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .config-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .config-item:last-child {{
            border-bottom: none;
        }}
        .config-label {{
            font-weight: 600;
            color: #555;
        }}
        .config-value {{
            color: #333;
            font-family: 'Courier New', monospace;
            background: white;
            padding: 5px 10px;
            border-radius: 5px;
            word-break: break-all;
        }}
        .password-hidden {{
            letter-spacing: 3px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👋 Hello World</h1>
        <p class="subtitle">Конфигурация приложения</p>
        
        <div class="section">
            <div class="section-title">🌐 Host Configuration</div>
            <div class="config-item">
                <span class="config-label">Host:</span>
                <span class="config-value">{host}</span>
            </div>
            <div class="config-item">
                <span class="config-label">Port:</span>
                <span class="config-value">{port}</span>
            </div>
            <div class="config-item">
                <span class="config-label">Debug:</span>
                <span class="config-value">{debug}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🗄️ Database Configuration</div>
            <div class="config-item">
                <span class="config-label">DB Host:</span>
                <span class="config-value">{db_host}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Port:</span>
                <span class="config-value">{db_port}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Name:</span>
                <span class="config-value">{db_name}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB User:</span>
                <span class="config-value">{db_user}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Password:</span>
                <span class="config-value password-hidden">{db_password_display}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB URL:</span>
                <span class="config-value">{db_url_display}</span>
            </div>
        </div>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
        return

