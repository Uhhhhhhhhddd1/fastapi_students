# app/db/models.py (ДОБАВЛЕНО)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base # Импортируем Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    students = relationship("Student", back_populates="group")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer)
    # ondelete="SET NULL" - при удалении группы, у студента group_id станет NULL
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True) # <--- nullable=True разрешает NULL
    group = relationship("Group", back_populates="students")