from http.server import BaseHTTPRequestHandler
import os
import sys
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from currency_parser import CurrencyParser
import plotly.graph_objects as go
import plotly.utils

# Загружаем переменные окружения
load_dotenv()

# Инициализируем парсер
parser = CurrencyParser()

def is_vercel():
    """Определяет, запущено ли приложение на Vercel"""
    return os.getenv('VERCEL') == '1' or 'vercel' in os.getenv('HOST', '').lower()

# Загружаем HTML шаблоны из app.py
# Для упрощения, копируем основные шаблоны
CURRENCY_HTML_TEMPLATE = open(os.path.join(os.path.dirname(__file__), '..', 'app.py'), 'r', encoding='utf-8').read()
# Извлекаем CURRENCY_HTML_TEMPLATE из app.py
currency_template_start = CURRENCY_HTML_TEMPLATE.find('CURRENCY_HTML_TEMPLATE = """')
currency_template_end = CURRENCY_HTML_TEMPLATE.find('"""', currency_template_start + len('CURRENCY_HTML_TEMPLATE = """')) + 3
CURRENCY_HTML = CURRENCY_HTML_TEMPLATE[currency_template_start + len('CURRENCY_HTML_TEMPLATE = """'):currency_template_end-3]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # Главная страница
        if path == '/' or path == '':
            self._serve_home_page()
        # Страница курсов валют
        elif path == '/currency':
            self._serve_currency_page()
        # API: список фонов
        elif path == '/api/backgrounds/list':
            self._serve_backgrounds_list()
        # API: текущие курсы
        elif path == '/api/currency/current':
            self._serve_currency_current(query_params)
        # API: история курсов
        elif path == '/api/currency/history':
            self._serve_currency_history(query_params)
        # Статические файлы фонов
        elif path.startswith('/static/backgrounds/'):
            self._serve_static_file(path)
        # Favicon
        elif path == '/favicon.ico':
            self._serve_favicon()
        else:
            self._serve_404()
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _serve_home_page(self):
        """Главная страница"""
        host = os.getenv('HOST', 'localhost')
        port = os.getenv('PORT', '8000')
        debug = os.getenv('DEBUG', 'False')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'test_db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        db_url = os.getenv('DB_URL', '')
        
        db_password_display = '*' * len(db_password) if db_password else 'Not set'
        db_url_display = db_url if db_url else 'Not set'
        
        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Configuration</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        h1 {{ color: #667eea; font-size: 3em; text-align: center; margin-bottom: 10px; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 40px; }}
        .section {{ margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #667eea; }}
        .section-title {{ font-size: 1.5em; color: #333; margin-bottom: 15px; font-weight: 600; }}
        .config-item {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e0e0e0; }}
        .config-item:last-child {{ border-bottom: none; }}
        .config-label {{ font-weight: 600; color: #555; }}
        .config-value {{ color: #333; font-family: 'Courier New', monospace; background: white; padding: 5px 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>👋 Hello World</h1>
        <p class="subtitle">Конфигурация приложения</p>
        <div class="section">
            <div class="section-title">🌐 Host Configuration</div>
            <div class="config-item"><span class="config-label">Host:</span><span class="config-value">{host}</span></div>
            <div class="config-item"><span class="config-label">Port:</span><span class="config-value">{port}</span></div>
            <div class="config-item"><span class="config-label">Debug:</span><span class="config-value">{debug}</span></div>
        </div>
        <div class="section">
            <div class="section-title">🗄️ Database Configuration</div>
            <div class="config-item"><span class="config-label">DB Host:</span><span class="config-value">{db_host}</span></div>
            <div class="config-item"><span class="config-label">DB Port:</span><span class="config-value">{db_port}</span></div>
            <div class="config-item"><span class="config-label">DB Name:</span><span class="config-value">{db_name}</span></div>
            <div class="config-item"><span class="config-label">DB User:</span><span class="config-value">{db_user}</span></div>
            <div class="config-item"><span class="config-label">DB Password:</span><span class="config-value">{db_password_display}</span></div>
            <div class="config-item"><span class="config-label">DB URL:</span><span class="config-value">{db_url_display}</span></div>
        </div>
    </div>
</body>
</html>"""
        self._send_html(html)
    
    def _serve_currency_page(self):
        """Страница с курсами валют"""
        # Читаем шаблон из файла app.py или используем встроенный
        try:
            app_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
            with open(app_path, 'r', encoding='utf-8') as f:
                content = f.read()
                start = content.find('CURRENCY_HTML_TEMPLATE = """')
                if start != -1:
                    start += len('CURRENCY_HTML_TEMPLATE = """')
                    end = content.find('"""', start)
                    if end != -1:
                        html = content[start:end]
                        self._send_html(html)
                        return
        except:
            pass
        
        # Fallback - простая страница
        self._send_html("<html><body><h1>Currency Page</h1><p>Loading...</p></body></html>")
    
    def _serve_backgrounds_list(self):
        """API: список фонов"""
        backgrounds_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'backgrounds')
        backgrounds = []
        
        env = 'vercel' if is_vercel() else 'localhost'
        prefix = 'vercel_bg' if is_vercel() else 'localhost_bg'
        
        if os.path.exists(backgrounds_dir):
            for file in os.listdir(backgrounds_dir):
                if file.startswith(prefix) and file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')):
                    backgrounds.append({
                        'filename': file,
                        'url': f'/static/backgrounds/{file}'
                    })
        
        self._send_json({
            'success': True,
            'environment': env,
            'backgrounds': backgrounds
        })
    
    def _serve_currency_current(self, params):
        """API: текущие курсы"""
        currency_type = params.get('type', ['fiat'])[0]
        
        if currency_type == 'fiat':
            rates = parser.get_all_fiat_rates()
        else:
            rates = parser.get_all_crypto_rates()
        
        self._send_json({
            'success': True,
            'rates': rates,
            'type': currency_type
        })
    
    def _serve_currency_history(self, params):
        """API: история курсов"""
        currency_code = params.get('currency', [''])[0].strip()
        period = params.get('period', ['7d'])[0]
        start_date_str = params.get('start_date', [None])[0]
        end_date_str = params.get('end_date', [None])[0]
        
        if not currency_code:
            self._send_json({'success': False, 'error': 'Не указана валюта'}, 400)
            return
        
        is_crypto = currency_code in parser.CRYPTO_CURRENCIES
        is_fiat = currency_code in parser.FIAT_CURRENCIES
        
        if not is_crypto and not is_fiat:
            self._send_json({'success': False, 'error': f'Валюта {currency_code} не поддерживается'}, 400)
            return
        
        end_date = datetime.now()
        
        if period == '7d':
            start_date = end_date - timedelta(days=7)
        elif period == '30d':
            start_date = end_date - timedelta(days=30)
        elif period == '90d':
            start_date = end_date - timedelta(days=90)
        elif period == '1y':
            start_date = end_date - timedelta(days=365)
        elif period == 'custom':
            if not start_date_str or not end_date_str:
                self._send_json({'success': False, 'error': 'Для кастомного периода необходимо указать начальную и конечную даты'}, 400)
                return
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                if start_date >= end_date:
                    self._send_json({'success': False, 'error': 'Начальная дата должна быть раньше конечной'}, 400)
                    return
            except ValueError as e:
                self._send_json({'success': False, 'error': f'Неверный формат даты: {str(e)}'}, 400)
                return
        else:
            start_date = end_date - timedelta(days=7)
        
        if is_crypto:
            max_crypto_days = 365
            period_days = (end_date - start_date).days
            if period_days > max_crypto_days:
                self._send_json({'success': False, 'error': f'Для криптовалют максимальный период составляет {max_crypto_days} дней'}, 400)
                return
        
        try:
            if is_crypto:
                history = parser.get_crypto_rates_history(currency_code, start_date, end_date)
            else:
                history = parser.get_fiat_rates_history(currency_code, start_date, end_date)
        except Exception as e:
            self._send_json({'success': False, 'error': f'Ошибка при получении данных: {str(e)}'}, 500)
            return
        
        if not history or len(history) == 0:
            self._send_json({'success': False, 'error': f'Не удалось получить данные за указанный период для валюты {currency_code}'}, 400)
            return
        
        dates = [item['date'].strftime('%Y-%m-%d') for item in history]
        rates = [item['rate'] for item in history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=rates,
            mode='lines+markers',
            name=currency_code,
            line=dict(color='#667eea', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=f'Курс {currency_code} к рублю',
            xaxis_title='Дата',
            yaxis_title='Курс (RUB)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            showlegend=False
        )
        
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        self._send_json({
            'success': True,
            'graph': graph_json,
            'data': {
                'dates': dates,
                'rates': rates,
                'min': min(rates),
                'max': max(rates),
                'current': rates[-1] if rates else None
            }
        })
    
    def _serve_static_file(self, path):
        """Отдача статических файлов"""
        filename = path.replace('/static/backgrounds/', '')
        file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'backgrounds', filename)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            if filename.endswith('.svg'):
                self.send_header('Content-Type', 'image/svg+xml')
            elif filename.endswith('.png'):
                self.send_header('Content-Type', 'image/png')
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                self.send_header('Content-Type', 'image/jpeg')
            else:
                self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        else:
            self._serve_404()
    
    def _serve_favicon(self):
        """Favicon"""
        self.send_response(200)
        self.send_header('Content-Type', 'image/vnd.microsoft.icon')
        self.end_headers()
        self.wfile.write(b'')
    
    def _serve_404(self):
        """404 ошибка"""
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>404 Not Found</h1></body></html>')
