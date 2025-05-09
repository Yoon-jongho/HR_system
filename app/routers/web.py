from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from typing import Optional

from app.database.database import get_db
from app.models import employee as employee_models
from app.models import department as department_models

router = APIRouter(
    prefix="/web",
    tags=["web interface"],
    include_in_schema=False,
)

templates = Jinja2Templates(directory=Path("app/templates"))

@router.get("/employees")
def list_employees(
    request: Request,
    db: Session = Depends(get_db),
    name: Optional[str] = None,
    department_id: Optional[int] = None,
):
    query = db.query(employee_models.Employee)

    if name:
        query = query.filter(employee_models.Employee.name.ilike(f"%{name}%"))
    
    if department_id:
        query = query.filter(employee_models.Employee.department_id == department_id)
    
    employees = query.all()
    departments = db.query(department_models.Department).all()

    return templates.TemplateResponse(
        "employees/list.html",
        {
            "request": request,
            "employees": employees,
            "departments": departments,
            "name": name,
            "department_id": department_id,
        }
    )

@router.get("/employees/create")
def create_employee_form(
    request: Request,
    db: Session = Depends(get_db),
):
    departments = db.query(department_models.Department).all()
    return templates.TemplateResponse(
        "employees/form.html",
        {
            "request": request,
            "departments": departments,
            "title": "직원 추가",
            "employee": None,
        }
    )

@router.get("/departments")
def list_departments(
    request: Request,
    db: Session = Depends(get_db),
 ):
    departments = db.query(department_models.Department).all()
    
    return templates.TemplateResponse(
        "departments/list.html",
        {
            "request": request,
            "departments": departments,
            "title": "부서 관리",
    
        }
)

@router.get("/login")
def login_form(
    request: Request,
):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        }
    )

@router.get("/departments/create")
def create_department_form(request: Request):
    return templates.TemplateResponse(
        "departments/form.html", 
        {
            "request": request, 
            "title": "부서 추가",
            "department": None
        }
    )

@router.get("/departments/{department_id}/edit")
def edit_department_form(request: Request, department_id: int, db: Session = Depends(get_db)):
    department = db.query(department_models.Department).filter(department_models.Department.id == department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return templates.TemplateResponse(
        "departments/form.html", 
        {
            "request": request, 
            "title": "부서 수정",
            "department": department
        }
    )

@router.get("/employees/{employee_id}/edit")
def edit_employee_form(request: Request, employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(employee_models.Employee).filter(employee_models.Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    departments = db.query(department_models.Department).all()
    
    return templates.TemplateResponse(
        "employees/form.html", 
        {
            "request": request, 
            "title": "직원 수정",
            "employee": employee,
            "departments": departments
        }
    )