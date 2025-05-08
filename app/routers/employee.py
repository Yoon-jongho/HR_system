from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from app.database.database import get_db
from app.models import employee as models, department as department_models
from app.schemas import employee as schemas, department as department_schemas
from app.routers.user import get_current_user
from app.models import user as user_models


router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):
    db_department = db.query(department_models.Department).filter(department_models.Department.id == employee.department_id).first()
    if db_department is None:
        raise HTTPException(status_code=400, detail="Department not found")

    db_employee = models.Employee(
        name=employee.name,
        department_id=employee.department_id,
        position=employee.position,
        hire_date=employee.hire_date,
        salary=employee.salary,
        email=employee.email,
        phone=employee.phone,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, 
                   limit: int = 100, 
                   name: Optional[str] = None, 
                   department_id: Optional[int] = None,
                   min_salary: Optional[float] = None,
                   max_salary: Optional[float] = None,
                   hired_after: Optional[str] = None, 
                   db: Session = Depends(get_db)
                   ):
    query = db.query(models.Employee)

    if name:
        query = query.filter(models.Employee.name.like(f"%{name}%"))
    
    if department_id:
        query = query.filter(models.Employee.department_id == department_id)

    if min_salary is not None:
        query = query.filter(models.Employee.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(models.Employee.salary <= max_salary)
    if hired_after:
        query = query.filter(models.Employee.hire_date >= hired_after)    
    
    employees = query.offset(skip).limit(limit).all()
    return employees

@router.get("/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee_data = employee.model_dump(exclude_unset=True)

    for key, value in employee_data.items():
        setattr(db_employee, key, value)
    
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_user: user_models.User = Depends(get_current_user)):

    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_employee)
    db.commit()
    return None

@router.get("/stats/departments", tags=["통계"])
def get_department_stats(db: Session = Depends(get_db)):
    stats = db.query(
        department_models.Department.name.label("department_name"),
        department_models.Department.id.label("department_id"),
        func.count(models.Employee.id).label("employee_count"),
        func.avg(models.Employee.salary).label("average_salary"),
    ).join(
        department_models.Department,
        models.Employee.department_id == department_models.Department.id,
    ).group_by(department_models.Department.id, department_models.Department.name).all()

    result = []
    for dept_name, dept_id, count, avg_salary in stats:
        result.append({
            "department_id": dept_id,
            "department_name": dept_name,
            "employee_count": count,
            "average_salary": float(avg_salary) if avg_salary else 0,
        })
    return result

