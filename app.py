#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from dotenv import load_dotenv
from datetime import datetime, timedelta
from currency_parser import CurrencyParser
import plotly.graph_objects as go
import plotly.utils
import json

# Загружаем переменные окружения из .env файла
load_dotenv()

app = Flask(__name__)
parser = CurrencyParser()

# Настройка статических файлов
app.config['STATIC_FOLDER'] = 'static'

# Получаем параметры хоста
host = os.getenv('HOST', 'localhost')
port = int(os.getenv('PORT', '8000'))
debug = os.getenv('DEBUG', 'False').lower() == 'true'

# Получаем параметры подключения к БД
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'test_db')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', '')
db_url = os.getenv('DB_URL', '')

# HTML шаблон
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World - Configuration</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            transition: background-image 0.5s ease;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            font-size: 3em;
            text-align: center;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .section-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .config-item {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        .config-item:last-child {
            border-bottom: none;
        }
        .config-label {
            font-weight: 600;
            color: #555;
        }
        .config-value {
            color: #333;
            font-family: 'Courier New', monospace;
            background: white;
            padding: 5px 10px;
            border-radius: 5px;
            word-break: break-all;
        }
        .password-hidden {
            letter-spacing: 3px;
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
            <select id="backgroundSelect" style="padding: 8px; border-radius: 5px; border: 1px solid #ddd; background: white;">
                <option value="">По умолчанию</option>
            </select>
        </div>
        <h1>👋 Hello World</h1>
        <p class="subtitle">Конфигурация приложения</p>
        
        <div class="section">
            <div class="section-title">🌐 Host Configuration</div>
            <div class="config-item">
                <span class="config-label">Host:</span>
                <span class="config-value">{{ host }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">Port:</span>
                <span class="config-value">{{ port }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">Debug:</span>
                <span class="config-value">{{ debug }}</span>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">🗄️ Database Configuration</div>
            <div class="config-item">
                <span class="config-label">DB Host:</span>
                <span class="config-value">{{ db_host }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Port:</span>
                <span class="config-value">{{ db_port }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Name:</span>
                <span class="config-value">{{ db_name }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB User:</span>
                <span class="config-value">{{ db_user }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB Password:</span>
                <span class="config-value password-hidden">{{ db_password }}</span>
            </div>
            <div class="config-item">
                <span class="config-label">DB URL:</span>
                <span class="config-value">{{ db_url }}</span>
            </div>
        </div>
    </div>
    <script>
        // Загрузка списка фонов
        async function loadBackgrounds() {
            try {
                const response = await fetch('/api/backgrounds/list');
                const data = await response.json();
                
                if (data.success && data.backgrounds.length > 0) {
                    const select = document.getElementById('backgroundSelect');
                    data.backgrounds.forEach(bg => {
                        const option = document.createElement('option');
                        option.value = bg.url;
                        option.textContent = bg.filename;
                        select.appendChild(option);
                    });
                    
                    // Загружаем сохраненный фон
                    const savedBg = localStorage.getItem('selectedBackground');
                    if (savedBg) {
                        select.value = savedBg;
                        applyBackground(savedBg);
                    }
                }
            } catch (error) {
                console.error('Ошибка загрузки фонов:', error);
            }
        }
        
        // Применение фона
        function applyBackground(url) {
            if (url) {
                document.body.style.backgroundImage = `url(${url})`;
                document.body.style.backgroundSize = 'cover';
                document.body.style.backgroundPosition = 'center';
                document.body.style.backgroundAttachment = 'fixed';
            } else {
                document.body.style.backgroundImage = '';
                document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }
        }
        
        // Обработка изменения фона
        document.getElementById('backgroundSelect').addEventListener('change', function() {
            const url = this.value;
            if (url) {
                localStorage.setItem('selectedBackground', url);
            } else {
                localStorage.removeItem('selectedBackground');
            }
            applyBackground(url);
        });
        
        // Загрузка при старте
        loadBackgrounds();
    </script>
</body>
</html>
"""

CURRENCY_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Курсы валют</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px;
            transition: background-image 0.5s ease;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            text-align: center;
            margin-bottom: 30px;
            font-weight: 700;
        }
        .nav-links {
            text-align: center;
            margin-bottom: 30px;
        }
        .nav-links a {
            color: #667eea;
            text-decoration: none;
            margin: 0 15px;
            font-weight: 500;
        }
        .nav-links a:hover {
            text-decoration: underline;
        }
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            align-items: center;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .control-group label {
            font-size: 0.9em;
            color: #666;
            font-weight: 500;
        }
        select, input[type="date"], button {
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            font-family: inherit;
        }
        select:focus, input[type="date"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        .custom-period {
            display: none;
            gap: 10px;
        }
        .custom-period.active {
            display: flex;
        }
        .chart-container {
            margin-top: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .stat-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        .stat-value {
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 1.1em;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .current-rates {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-bottom: 30px;
        }
        .rate-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .rate-code {
            font-weight: 700;
            color: #667eea;
            font-size: 1.1em;
        }
        .rate-value {
            margin-top: 5px;
            font-size: 1.3em;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
            <select id="backgroundSelect" style="padding: 8px; border-radius: 5px; border: 1px solid #ddd; background: white;">
                <option value="">По умолчанию</option>
            </select>
        </div>
        <h1>💱 Курсы валют к рублю</h1>
        
        <div class="nav-links">
            <a href="/">🏠 Главная</a>
            <a href="/currency">💱 Курсы валют</a>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label>Тип валюты</label>
                <select id="currencyType">
                    <option value="fiat">Фиатные валюты</option>
                    <option value="crypto">Криптовалюты</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>Валюта</label>
                <select id="currencySelect"></select>
            </div>
            
            <div class="control-group">
                <label>Период</label>
                <select id="periodSelect">
                    <option value="7d">7 дней</option>
                    <option value="30d">30 дней</option>
                    <option value="90d">90 дней</option>
                    <option value="1y">1 год</option>
                    <option value="custom">Кастомный период</option>
                </select>
            </div>
            
            <div class="custom-period" id="customPeriod">
                <div class="control-group">
                    <label>Начальная дата</label>
                    <input type="date" id="startDate">
                </div>
                <div class="control-group">
                    <label>Конечная дата</label>
                    <input type="date" id="endDate">
                </div>
            </div>
            
            <div class="control-group">
                <label>&nbsp;</label>
                <button onclick="loadChart()">Показать график</button>
            </div>
        </div>
        
        <div id="currentRates" class="current-rates"></div>
        
        <div id="chartContainer" class="chart-container">
            <div class="loading">Выберите валюту и период для отображения графика</div>
        </div>
    </div>
    
    <script>
        const fiatCurrencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'AUD', 'CAD', 'NOK', 'SEK'];
        const cryptoCurrencies = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 'MATIC', 'LTC'];
        
        let currentRatesData = {};
        
        // Загрузка текущих курсов
        async function loadCurrentRates() {
            const type = document.getElementById('currencyType').value;
            const response = await fetch(`/api/currency/current?type=${type}`);
            const data = await response.json();
            
            if (data.success) {
                currentRatesData = data.rates;
                displayCurrentRates(data.rates);
                updateCurrencySelect(type);
            }
        }
        
        // Отображение текущих курсов
        function displayCurrentRates(rates) {
            const container = document.getElementById('currentRates');
            container.innerHTML = '';
            
            for (const [code, rate] of Object.entries(rates)) {
                const card = document.createElement('div');
                card.className = 'rate-card';
                card.innerHTML = `
                    <div class="rate-code">${code}</div>
                    <div class="rate-value">${rate.toLocaleString('ru-RU', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</div>
                `;
                container.appendChild(card);
            }
        }
        
        // Обновление списка валют
        function updateCurrencySelect(type) {
            const select = document.getElementById('currencySelect');
            select.innerHTML = '';
            
            const currencies = type === 'fiat' ? fiatCurrencies : cryptoCurrencies;
            currencies.forEach(code => {
                const option = document.createElement('option');
                option.value = code;
                option.textContent = code;
                select.appendChild(option);
            });
        }
        
        // Загрузка графика
        async function loadChart() {
            const currency = document.getElementById('currencySelect').value;
            const period = document.getElementById('periodSelect').value;
            const container = document.getElementById('chartContainer');
            
            // Проверка выбранной валюты
            if (!currency) {
                container.innerHTML = '<div class="error">Пожалуйста, выберите валюту</div>';
                return;
            }
            
            container.innerHTML = '<div class="loading">Загрузка данных...</div>';
            
            let url = `/api/currency/history?currency=${encodeURIComponent(currency)}&period=${encodeURIComponent(period)}`;
            
            if (period === 'custom') {
                const startDate = document.getElementById('startDate').value;
                const endDate = document.getElementById('endDate').value;
                
                if (!startDate || !endDate) {
                    container.innerHTML = '<div class="error">Пожалуйста, выберите начальную и конечную даты</div>';
                    return;
                }
                
                url += `&start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`;
            }
            
            try {
                const response = await fetch(url);
                const data = await response.json();
                
                if (data.success) {
                    const graphData = JSON.parse(data.graph);
                    
                    // Добавляем статистику
                    const statsHtml = `
                        <div class="stats">
                            <div class="stat-card">
                                <div class="stat-label">Текущий курс</div>
                                <div class="stat-value">${data.data.current.toLocaleString('ru-RU', {minimumFractionDigits: 2})} ₽</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-label">Минимальный</div>
                                <div class="stat-value">${data.data.min.toLocaleString('ru-RU', {minimumFractionDigits: 2})} ₽</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-label">Максимальный</div>
                                <div class="stat-value">${data.data.max.toLocaleString('ru-RU', {minimumFractionDigits: 2})} ₽</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-label">Изменение</div>
                                <div class="stat-value" style="color: ${data.data.current >= data.data.min ? '#0a0' : '#c33'}">
                                    ${((data.data.current - data.data.min) / data.data.min * 100).toFixed(2)}%
                                </div>
                            </div>
                        </div>
                    `;
                    container.innerHTML = '<div id="chart"></div>' + statsHtml;
                    Plotly.newPlot('chart', graphData.data, graphData.layout, {responsive: true});
                } else {
                    container.innerHTML = `<div class="error">Ошибка: ${data.error || 'Не удалось загрузить данные'}</div>`;
                }
            } catch (error) {
                container.innerHTML = `<div class="error">Ошибка подключения: ${error.message}</div>`;
            }
        }
        
        // Обработка изменения типа валюты
        document.getElementById('currencyType').addEventListener('change', () => {
            loadCurrentRates();
        });
        
        // Обработка изменения периода
        document.getElementById('periodSelect').addEventListener('change', function() {
            const customPeriod = document.getElementById('customPeriod');
            if (this.value === 'custom') {
                customPeriod.classList.add('active');
            } else {
                customPeriod.classList.remove('active');
            }
        });
        
        // Загрузка списка фонов
        async function loadBackgrounds() {
            try {
                const response = await fetch('/api/backgrounds/list');
                const data = await response.json();
                
                if (data.success && data.backgrounds.length > 0) {
                    const select = document.getElementById('backgroundSelect');
                    data.backgrounds.forEach(bg => {
                        const option = document.createElement('option');
                        option.value = bg.url;
                        option.textContent = bg.filename;
                        select.appendChild(option);
                    });
                    
                    // Загружаем сохраненный фон
                    const savedBg = localStorage.getItem('selectedBackground');
                    if (savedBg) {
                        select.value = savedBg;
                        applyBackground(savedBg);
                    }
                }
            } catch (error) {
                console.error('Ошибка загрузки фонов:', error);
            }
        }
        
        // Применение фона
        function applyBackground(url) {
            if (url) {
                document.body.style.backgroundImage = `url(${url})`;
                document.body.style.backgroundSize = 'cover';
                document.body.style.backgroundPosition = 'center';
                document.body.style.backgroundAttachment = 'fixed';
            } else {
                document.body.style.backgroundImage = '';
                document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            }
        }
        
        // Обработка изменения фона
        document.getElementById('backgroundSelect').addEventListener('change', function() {
            const url = this.value;
            if (url) {
                localStorage.setItem('selectedBackground', url);
            } else {
                localStorage.removeItem('selectedBackground');
            }
            applyBackground(url);
        });
        
        // Инициализация
        loadCurrentRates();
        loadBackgrounds();
        
        // Устанавливаем даты по умолчанию для кастомного периода
        const today = new Date();
        const weekAgo = new Date(today);
        weekAgo.setDate(today.getDate() - 7);
        
        document.getElementById('endDate').value = today.toISOString().split('T')[0];
        document.getElementById('startDate').value = weekAgo.toISOString().split('T')[0];
    </script>
</body>
</html>
"""

@app.route('/favicon.ico')
def favicon():
    """Endpoint для favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    db_password_display = '*' * len(db_password) if db_password else 'Not set'
    return render_template_string(
        HTML_TEMPLATE,
        host=host,
        port=port,
        debug=debug,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        db_user=db_user,
        db_password=db_password_display,
        db_url=db_url if db_url else 'Not set'
    )

def is_vercel():
    """Определяет, запущено ли приложение на Vercel"""
    return os.getenv('VERCEL') == '1' or 'vercel' in os.getenv('HOST', '').lower()

@app.route('/static/backgrounds/<path:filename>')
def background_file(filename):
    """Endpoint для отдачи файлов фонов"""
    return send_from_directory(os.path.join(app.root_path, 'static', 'backgrounds'), filename)

@app.route('/api/backgrounds/list')
def api_backgrounds_list():
    """API для получения списка доступных фонов"""
    backgrounds_dir = os.path.join(app.root_path, 'static', 'backgrounds')
    backgrounds = []
    
    # Определяем окружение
    env = 'vercel' if is_vercel() else 'localhost'
    prefix = 'vercel_bg' if is_vercel() else 'localhost_bg'
    
    if os.path.exists(backgrounds_dir):
        for file in os.listdir(backgrounds_dir):
            # Фильтруем только файлы для текущего окружения
            if file.startswith(prefix) and file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')):
                backgrounds.append({
                    'filename': file,
                    'url': f'/static/backgrounds/{file}'
                })
    
    return jsonify({
        'success': True,
        'environment': env,
        'backgrounds': backgrounds
    })

@app.route('/currency')
def currency():
    """Страница с курсами валют"""
    return render_template_string(CURRENCY_HTML_TEMPLATE)

@app.route('/api/currency/current')
def api_currency_current():
    """API для получения текущих курсов"""
    currency_type = request.args.get('type', 'fiat')  # fiat или crypto
    
    if currency_type == 'fiat':
        rates = parser.get_all_fiat_rates()
    else:
        rates = parser.get_all_crypto_rates()
    
    return jsonify({
        'success': True,
        'rates': rates,
        'type': currency_type
    })

@app.route('/api/currency/history')
def api_currency_history():
    """API для получения истории курсов"""
    currency_code = request.args.get('currency', '').strip()
    period = request.args.get('period', '7d')  # 7d, 30d, 90d, 1y, custom
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    # Проверка наличия валюты
    if not currency_code:
        return jsonify({
            'success': False,
            'error': 'Не указана валюта'
        }), 400
    
    # Проверка, что валюта существует
    is_crypto = currency_code in parser.CRYPTO_CURRENCIES
    is_fiat = currency_code in parser.FIAT_CURRENCIES
    
    if not is_crypto and not is_fiat:
        return jsonify({
            'success': False,
            'error': f'Валюта {currency_code} не поддерживается'
        }), 400
    
    # Определяем период
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
            return jsonify({
                'success': False,
                'error': 'Для кастомного периода необходимо указать начальную и конечную даты'
            }), 400
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            # Проверка, что начальная дата раньше конечной
            if start_date >= end_date:
                return jsonify({
                    'success': False,
                    'error': 'Начальная дата должна быть раньше конечной'
                }), 400
            
            # Ограничение на максимальный период (например, 5 лет)
            max_days = 1825  # 5 лет
            if (end_date - start_date).days > max_days:
                return jsonify({
                    'success': False,
                    'error': f'Максимальный период не должен превышать {max_days // 365} лет'
                }), 400
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Неверный формат даты: {str(e)}'
            }), 400
    else:
        start_date = end_date - timedelta(days=7)
    
    # Для криптовалют ограничиваем максимальный период (CoinGecko лимиты)
    if is_crypto:
        max_crypto_days = 365  # 1 год для криптовалют
        period_days = (end_date - start_date).days
        if period_days > max_crypto_days:
            return jsonify({
                'success': False,
                'error': f'Для криптовалют максимальный период составляет {max_crypto_days} дней. Выбранный период: {period_days} дней'
            }), 400
        
        # Также проверяем, что дата не слишком старая (CoinGecko хранит данные примерно с 2013 года)
        min_crypto_date = datetime(2013, 1, 1)
        if start_date < min_crypto_date:
            return jsonify({
                'success': False,
                'error': f'Минимальная дата для криптовалют: {min_crypto_date.strftime("%Y-%m-%d")}'
            }), 400
    
    # Получаем данные
    try:
        if is_crypto:
            history = parser.get_crypto_rates_history(currency_code, start_date, end_date)
        else:
            history = parser.get_fiat_rates_history(currency_code, start_date, end_date)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Ошибка при получении данных: {str(e)}'
        }), 500
    
    if not history or len(history) == 0:
        error_msg = f'Не удалось получить данные за указанный период для валюты {currency_code}'
        if is_crypto:
            error_msg += '. Возможно, период слишком большой или CoinGecko API временно недоступен. Попробуйте уменьшить период.'
        else:
            error_msg += '. Возможно, указанный период выходит за пределы доступных данных ЦБ РФ.'
        return jsonify({
            'success': False,
            'error': error_msg
        }), 400
    
    # Формируем данные для графика
    dates = [item['date'].strftime('%Y-%m-%d') for item in history]
    rates = [item['rate'] for item in history]
    
    # Создаем график
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
    
    return jsonify({
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

if __name__ == '__main__':
    print(f"\n🚀 Запуск сервера на http://{host}:{port}")
    print(f"📊 Debug режим: {debug}")
    print(f"\nОткройте в браузере: http://{host}:{port}\n")
    app.run(host=host, port=port, debug=debug)

