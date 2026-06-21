cat << 'EOF' > Dockerfile
# Используем легковесный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения, чтобы Python не кешировал файлы и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем и переходим в рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для компиляции некоторых пакетов (например, psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip и копируем файл зависимостей
RUN pip install --upgrade pip
COPY requirements.txt /app/

# Устанавливаем библиотеки
RUN pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . /app/

# Запускаем сервер при старте контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EOF