from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = (
    Path(sys.executable).resolve().parent
    if getattr(sys, "frozen", False)
    else PROJECT_ROOT
)
load_dotenv(RUNTIME_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    database_url: str
    export_directory: Path = RUNTIME_ROOT / "data"


def get_settings() -> Settings:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    database = os.getenv("DB_NAME", "research_management")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "root")
    database_url = URL.create(
        "postgresql+psycopg",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=database,
    ).render_as_string(hide_password=False)
    return Settings(database_url=database_url)
