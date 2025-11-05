from http.server import BaseHTTPRequestHandler
import json
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
        
        # Формируем ответ
        response = {
            'message': 'Hello World',
            'host_config': {
                'host': host,
                'port': port,
                'debug': debug
            },
            'database_config': {
                'db_host': db_host,
                'db_port': db_port,
                'db_name': db_name,
                'db_user': db_user,
                'db_password': '*' * len(db_password) if db_password else 'Not set',
                'db_url': db_url if db_url else 'Not set'
            }
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
        return

