from contextlib import asynccontextmanager

from controllers import router
from database import Base, engine
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 로직
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 로직


# FastAPI 애플리케션 초기화
app = FastAPI(lifespan=app_lifespan, docs_url=None, redoc_url=None)  # Swagger UI, Redoc 비활성화
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
app.include_router(router)
templates = Jinja2Templates(directory="templates")


# 기본 라우트
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)
