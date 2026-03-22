# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установим зависимости системы
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем проект
COPY . .

# По умолчанию не запускаем ничего — используем docker-compose command