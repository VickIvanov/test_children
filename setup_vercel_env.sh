#!/bin/bash

# Скрипт для добавления переменных окружения в Vercel проект test_children

echo "Добавление переменных окружения в Vercel..."

# Host Configuration
vercel env add HOST production <<< "localhost"
vercel env add PORT production <<< "8000"
vercel env add DEBUG production <<< "True"

# Database Configuration
vercel env add DB_HOST production <<< "localhost"
vercel env add DB_PORT production <<< "5432"
vercel env add DB_NAME production <<< "test_db"
vercel env add DB_USER production <<< "postgres"
read -sp "Введите пароль БД: " db_password
vercel env add DB_PASSWORD production <<< "$db_password"
vercel env add DB_URL production <<< "postgresql://postgres:$db_password@localhost:5432/test_db"

# Также добавляем для preview и development окружений
echo "Добавление переменных для preview окружения..."
vercel env add HOST preview <<< "localhost"
vercel env add PORT preview <<< "8000"
vercel env add DEBUG preview <<< "True"
vercel env add DB_HOST preview <<< "localhost"
vercel env add DB_PORT preview <<< "5432"
vercel env add DB_NAME preview <<< "test_db"
vercel env add DB_USER preview <<< "postgres"
vercel env add DB_PASSWORD preview <<< "$db_password"
vercel env add DB_URL preview <<< "postgresql://postgres:$db_password@localhost:5432/test_db"

echo "Добавление переменных для development окружения..."
vercel env add HOST development <<< "localhost"
vercel env add PORT development <<< "8000"
vercel env add DEBUG development <<< "True"
vercel env add DB_HOST development <<< "localhost"
vercel env add DB_PORT development <<< "5432"
vercel env add DB_NAME development <<< "test_db"
vercel env add DB_USER development <<< "postgres"
vercel env add DB_PASSWORD development <<< "$db_password"
vercel env add DB_URL development <<< "postgresql://postgres:$db_password@localhost:5432/test_db"

echo "Готово! Переменные окружения добавлены."

