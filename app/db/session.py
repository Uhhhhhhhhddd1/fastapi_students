# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL  # Используем URL из конфига

# Создаём движок подключения к БД
engine = create_engine(DATABASE_URL)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

# Класс сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция-зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()