# 1. Базовый образ (берём лёгкую версию Python)
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь код проекта в контейнер
COPY . .

# 5. Открываем порт, на котором работает FastAPI
EXPOSE 8000

# 6. Команда запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]