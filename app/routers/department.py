from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.database import get_db
from app.models import department as models
from app.schemas import department as schemas

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Department, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = db.query(models.Department).filter(
        models.Department.name == department.name
    ).first()

    if db_department:
        raise HTTPException(
            status_code=400,
            detail="Department with this name already exists",
        )
    
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

@router.get("/", response_model=List[schemas.Department])
def read_departments(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Department)

    if name:
        query = query.filter(models.Department.name.like(f"%{name}%"))

    departments = query.offset(skip).limit(limit).all()
    return departments

@router.get("/{department_id}", response_model=schemas.Department)
def read_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.put("/{department_id}", response_model=schemas.Department)
def update_department(
    department_id: int,
    department: schemas.DepartmentUpdate,
    db: Session = Depends(get_db)
):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    update_data = department.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_department, key, value)
    
    db.commit()
    db.refresh(db_department)
    return db_department

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    db: Session = Depends(get_db)
):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()

    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(db_department)
    db.commit()
    return None

