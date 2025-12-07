# app/main.py (ИСПРАВЛЕНО)
from fastapi import FastAPI
from app.api.routers import students, groups
from app.db import init_db # <--- ДОБАВЛЕНО

# Инициализируем БД (создаем таблицы, если их нет)
init_db() # <--- ВЫЗЫВАЕМ ФУНКЦИЮ

app = FastAPI(title="Students API", version="1.0")

app.include_router(students.router)
app.include_router(groups.router)

# Для проверки, что сервер живой
@app.get("/")
def read_root():
    return {"message": "Students API is running!"}