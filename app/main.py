from fastapi import FastAPI
from app.database.database import engine, Base
from app.routers import employee, department, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="이노 인사 관리 시스템",
    description="이노 인사 관리 시스템 API 입니다.",
    version="0.1.0",
)

app.include_router(employee.router)
app.include_router(department.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message : 이노 인사 관리 시스템에 오신 것을 환영합니다."}

# @app.get(("/items/{item_id}"))
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}