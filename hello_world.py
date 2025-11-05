#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

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

# Выводим Hello World
print("Hello World")

# Выводим информацию о конфигурации
print("\n=== Host Configuration ===")
print(f"Host: {host}")
print(f"Port: {port}")
print(f"Debug: {debug}")

print("\n=== Database Configuration ===")
print(f"DB Host: {db_host}")
print(f"DB Port: {db_port}")
print(f"DB Name: {db_name}")
print(f"DB User: {db_user}")
print(f"DB Password: {'*' * len(db_password) if db_password else 'Not set'}")
print(f"DB URL: {db_url if db_url else 'Not set'}")

