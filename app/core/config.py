# app/core/config.py (ИСПРАВЛЕНО)
import os
# from dotenv import load_dotenv # <-- УДАЛЕНО

# load_dotenv()  # <-- УДАЛЕНО

# Используем переменную, переданную Docker Compose
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Добавляем явную ошибку для диагностики, если переменная пустая
    raise ValueError("DATABASE_URL environment variable is not set. Check your .env file or docker-compose environment block.")