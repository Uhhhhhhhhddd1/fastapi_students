# app/db/schemas.py (Исправленный)
from pydantic import BaseModel
from typing import List, Optional

class StudentBase(BaseModel):
    name: str
    age: int # <--- ДОБАВЛЕНО

class StudentCreate(StudentBase):
    group_id: Optional[int] = None # Теперь можно создавать студента сразу в группе

class Student(StudentBase):
    id: int
    group_id: Optional[int] = None

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class Group(GroupBase):
    id: int

    class Config:
        from_attributes = True

class GroupWithStudents(Group):
    students: List[Student] = []

class TransferRequest(BaseModel):
    new_group_id: int