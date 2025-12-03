from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db, schemas, crud

router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Group, status_code=status.HTTP_201_CREATED)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)

@router.get("/{group_id}", response_model=schemas.GroupWithStudents)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud.get_group(db=db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

@router.get("/", response_model=list[schemas.Group])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    groups = crud.get_groups(db=db, skip=skip, limit=limit)
    return groups

@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    success = crud.delete_group(db=db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return None

@router.post("/{group_id}/students/{student_id}", response_model=schemas.Student)
def add_student_to_group(group_id: int, student_id: int, db: Session = Depends(get_db)):
    student = crud.add_student_to_group(db=db, student_id=student_id, group_id=group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student or group not found")
    return student

@router.delete("/{group_id}/students/{student_id}", response_model=schemas.Student)
def remove_student_from_group(group_id: int, student_id: int, db: Session = Depends(get_db)):
    student = crud.remove_student_from_group(db=db, student_id=student_id, group_id=group_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not in this group")
    return student

@router.get("/{group_id}/students/", response_model=list[schemas.Student])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = crud.get_students_in_group(db=db, group_id=group_id)
    return students