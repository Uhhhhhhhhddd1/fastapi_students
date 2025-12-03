# app/db/crud.py
from sqlalchemy.orm import Session
import app.db.models as models
import app.db.schemas as schemas

# --- Students CRUD ---

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        name=student.name, 
        age=student.age,
        group_id=student.group_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def delete_student(db: Session, student_id: int) -> bool:
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

# --- Groups CRUD ---

def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(name=group.name)
    db.add(db_group)
    try:
        db.commit()
        db.refresh(db_group)
        return db_group
    except Exception:
        db.rollback()
        return None # На случай, если имя группы уже существует

def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Group).offset(skip).limit(limit).all()

def delete_group(db: Session, group_id: int) -> bool:
    db_group = get_group(db, group_id)
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False

# --- Relationship Logic ---

def add_student_to_group(db: Session, student_id: int, group_id: int):
    student = get_student(db, student_id)
    group = get_group(db, group_id)
    if not student or not group:
        return None
    
    student.group_id = group_id
    db.commit()
    db.refresh(student)
    return student

def remove_student_from_group(db: Session, student_id: int, group_id: int):
    # Убеждаемся, что студент есть и принадлежит именно этой группе
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.group_id == group_id
    ).first()
    
    if not student:
        return None
    
    student.group_id = None
    db.commit()
    db.refresh(student)
    return student

def get_students_in_group(db: Session, group_id: int):
    return db.query(models.Student).filter(models.Student.group_id == group_id).all()

def transfer_student(db: Session, student_id: int, new_group_id: int):
    # Логика перевода: просто присваиваем новый group_id
    return add_student_to_group(db, student_id, new_group_id)