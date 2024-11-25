# Базовый образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Команда для запуска сервера разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
