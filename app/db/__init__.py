# app/db/__init__.py (ИСПРАВЛЕНО)
# Просто экспортируем нужные объекты
from .database import get_db, Base, engine # engine и Base теперь здесь
from . import models, schemas, crud # Экспортируем модули

def init_db():
    # Важно: импортируем models здесь, чтобы Base знал, какие таблицы создать
    import app.db.models 
    Base.metadata.create_all(bind=engine)