from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

# alembic -> 마이그레이션 관리 도구 (추후 참고 충돌 에러 방지)

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    position = Column(String(100))
    hire_date = Column(Date)
    salary = Column(Float)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), nullable=True)

    department = relationship("Department", back_populates="employees")
