from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.database.database import engine, Base
from app.routers import employee, department, user, auth, web

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="이노 인사 관리 시스템",
    description="이노 인사 관리 시스템 API 입니다.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory=Path("app/templates"))

app.include_router(employee.router)
app.include_router(department.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(web.router)

@app.get("/", include_in_schema=False)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "이노 인사 관리 시스템",
            "description": "이노 인사 관리 시스템 API 입니다.",
        },
    )

# @app.get(("/items/{item_id}"))
# def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "q": q}