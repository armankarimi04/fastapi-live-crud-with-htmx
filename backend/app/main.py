from typing import Any
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.api.router import router as api_router
from app.api.views import router as views_router
from .database import init_async_db, async_engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    await init_async_db()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan, docs_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
# -> /static/css/style.css would serve the file from ./static/css/style.css


# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent
# app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
# example file that will be served: /static/dist/assets/main-C8x93abc.js


app.include_router(api_router, prefix="/api")
app.include_router(views_router, prefix="/views")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="API Docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
    )


@app.get("/")
def root():
    return "root"
