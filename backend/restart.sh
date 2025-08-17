#!/bin/bash

# Проверяем, запущен ли Docker Compose
if [ "$(docker compose ps -q)" ]; then
    echo "Docker Compose уже запущен. Останавливаем..."
    docker compose down
    echo "Пересобираем и запускаем заново..."
    docker compose up --build -d
else
    echo "Запускаем Docker Compose..."
    docker compose up -d
fi
