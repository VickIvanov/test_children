# Инструкция по настройке проекта на Vercel

## Шаг 1: Авторизация в Vercel

Выполните команду для авторизации:
```bash
vercel login
```

Следуйте инструкциям в браузере для завершения авторизации.

## Шаг 2: Создание проекта на Vercel

### Вариант A: Через CLI (рекомендуется)

```bash
vercel --yes
```

Следуйте инструкциям:
- Выберите "Link to existing project" или "Create new project"
- Введите название проекта: `test_children`
- Выберите настройки по умолчанию или настройте по необходимости

### Вариант B: Через веб-интерфейс

1. Откройте https://vercel.com
2. Перейдите в Dashboard
3. Нажмите "Add New Project"
4. Импортируйте репозиторий `VickIvanov/test_children` из GitHub
5. Назовите проект `test_children`
6. Нажмите "Deploy"

## Шаг 3: Добавление переменных окружения

После создания проекта выполните:

```bash
./setup_vercel_env.sh
```

Или добавьте переменные вручную через веб-интерфейс:
1. Откройте проект на Vercel
2. Перейдите в Settings → Environment Variables
3. Добавьте следующие переменные:

### Host Configuration
- `HOST` = `localhost`
- `PORT` = `8000`
- `DEBUG` = `True`

### Database Configuration
- `DB_HOST` = `localhost`
- `DB_PORT` = `5432`
- `DB_NAME` = `test_db`
- `DB_USER` = `postgres`
- `DB_PASSWORD` = `ваш_пароль`
- `DB_URL` = `postgresql://postgres:ваш_пароль@localhost:5432/test_db`

**Важно:** Добавьте переменные для всех окружений (Production, Preview, Development).

## Шаг 4: Деплой

После настройки переменных окружения проект автоматически задеплоится, если вы используете Git integration. 

Или выполните деплой вручную:
```bash
vercel --prod
```

## Проверка работы

После деплоя откройте URL вашего проекта (будет показан после деплоя) и вы должны увидеть JSON ответ с конфигурацией.

