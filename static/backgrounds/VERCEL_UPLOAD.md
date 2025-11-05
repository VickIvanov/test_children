# Инструкция по загрузке фонов в Vercel

## Способ 1: Автоматическая загрузка через Git (рекомендуется)

1. **Добавьте файлы фонов в папку `static/backgrounds/`**
   ```bash
   # Пример: скопируйте ваши файлы фонов
   cp ~/Downloads/my_background.jpg static/backgrounds/
   ```

2. **Закоммитьте и запушьте в Git**
   ```bash
   git add static/backgrounds/
   git commit -m "Add background images"
   git push
   ```

3. **Vercel автоматически задеплоит изменения**
   - Файлы будут доступны по URL: `https://your-project.vercel.app/static/backgrounds/filename.jpg`

## Способ 2: Загрузка через Vercel CLI

1. **Убедитесь, что вы авторизованы**
   ```bash
   vercel login
   ```

2. **Загрузите файлы через команду деплоя**
   ```bash
   # Добавьте файлы в папку static/backgrounds/, затем:
   vercel --prod
   ```

## Способ 3: Загрузка через веб-интерфейс Vercel

1. Откройте проект на https://vercel.com
2. Перейдите в раздел "Storage" или используйте Vercel Blob Storage
3. Загрузите файлы через интерфейс

## Способ 4: Использование Vercel Blob Storage (для больших файлов)

1. **Установите Vercel Blob**
   ```bash
   npm install @vercel/blob
   ```

2. **Загрузите файлы программно**
   ```python
   from vercel_blob import put
   
   # Загрузка файла
   blob = put("background.jpg", open("background.jpg", "rb"))
   # URL будет доступен через blob.url
   ```

## Важные замечания:

- **Размер файлов**: Vercel рекомендует файлы не более 4.5 MB для статических файлов
- **Форматы**: Поддерживаются JPG, PNG, WebP, GIF
- **Оптимизация**: Рекомендуется оптимизировать изображения перед загрузкой
- **Кеширование**: Vercel автоматически кеширует статические файлы

## Проверка загрузки:

После загрузки проверьте доступность файла:
```bash
curl https://your-project.vercel.app/static/backgrounds/filename.jpg
```

Или откройте в браузере:
```
https://your-project.vercel.app/static/backgrounds/filename.jpg
```

