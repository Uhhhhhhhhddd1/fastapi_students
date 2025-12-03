from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db, schemas, crud

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@router.get("/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db=db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/", response_model=list[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db=db, skip=skip, limit=limit)
    return students

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = crud.delete_student(db=db, student_id=student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

@router.patch("/{student_id}/transfer", response_model=schemas.Student)
def transfer_student(
    student_id: int,
    transfer: schemas.TransferRequest,
    db: Session = Depends(get_db)
):
    student = crud.transfer_student(db=db, student_id=student_id, new_group_id=transfer.new_group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return student