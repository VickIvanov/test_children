#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для добавления переменных окружения из .env файла в Vercel проект
Требует: vercel CLI и авторизацию
"""

import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

def add_env_var(name, value, environment='production'):
    """Добавляет переменную окружения в Vercel"""
    try:
        # Используем echo для передачи значения
        cmd = f'echo "{value}" | vercel env add {name} {environment}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ {name} ({environment}) добавлена")
            return True
        else:
            print(f"✗ Ошибка при добавлении {name} ({environment}): {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Исключение при добавлении {name}: {e}")
        return False

def main():
    print("Добавление переменных окружения в Vercel...")
    print("=" * 50)
    
    # Проверяем авторизацию
    try:
        result = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Ошибка: Необходима авторизация в Vercel")
            print("Выполните: vercel login")
            return
        print(f"Авторизован как: {result.stdout.strip()}")
    except Exception as e:
        print(f"Ошибка проверки авторизации: {e}")
        return
    
    # Переменные для добавления
    env_vars = {
        'HOST': os.getenv('HOST', 'localhost'),
        'PORT': os.getenv('PORT', '8000'),
        'DEBUG': os.getenv('DEBUG', 'True'),
        'DB_HOST': os.getenv('DB_HOST', 'localhost'),
        'DB_PORT': os.getenv('DB_PORT', '5432'),
        'DB_NAME': os.getenv('DB_NAME', 'test_db'),
        'DB_USER': os.getenv('DB_USER', 'postgres'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD', ''),
        'DB_URL': os.getenv('DB_URL', ''),
    }
    
    environments = ['production', 'preview', 'development']
    
    for env_name in environments:
        print(f"\nДобавление переменных для окружения: {env_name}")
        print("-" * 50)
        
        for var_name, var_value in env_vars.items():
            # Для DB_URL используем значение из .env или формируем из других переменных
            if var_name == 'DB_URL' and not var_value:
                db_user = env_vars['DB_USER']
                db_pass = env_vars['DB_PASSWORD']
                db_host = env_vars['DB_HOST']
                db_port = env_vars['DB_PORT']
                db_name = env_vars['DB_NAME']
                var_value = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
            
            add_env_var(var_name, var_value, env_name)
    
    print("\n" + "=" * 50)
    print("Готово! Переменные окружения добавлены.")
    print("\nДля применения изменений выполните:")
    print("  vercel --prod")

if __name__ == '__main__':
    main()

