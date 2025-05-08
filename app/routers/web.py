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