from __future__ import annotations

import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

from ..database import initialize_database
from ..services.auth_service import AuthService

WEB_ROOT = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=WEB_ROOT / "templates")

app = FastAPI(
    title="Research Paper Information Management System",
    version="1.0.0",
)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("APP_SECRET_KEY", "change-this-development-secret"),
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=False,
)
app.mount("/static", StaticFiles(directory=WEB_ROOT / "static"), name="static")

from . import routes  # noqa: E402,F401


def prepare_application() -> None:
    initialize_database()
    AuthService().ensure_default_admin()


def run_server() -> None:
    prepare_application()
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    uvicorn.run(
        "research_manager.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    run_server()
