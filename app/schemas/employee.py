from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

from app.schemas.department import Department

class EmployeeBase(BaseModel):
    name: str
    department_id: int
    position: str
    hire_date: date
    salary: float
    email: str
    phone: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = None
    department_id: Optional[int] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    salary: Optional[float] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class Employee(EmployeeBase):
    id: int
    department: Optional[Department] = None

    class Config:
        from_attributes = True
