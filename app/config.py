# Configuración centralizada de la aplicación.

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "instance" / "f2p_catalog.db"

load_dotenv(BASE_DIR / ".env")


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DEFAULT_SQLITE_PATH}"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY") or (
        "dev-secret-key-change-me" if FLASK_ENV == "development" else None
    )

    FREETOGAME_API_URL = os.getenv(
        "FREETOGAME_API_URL", "https://www.freetogame.com/api"
    )
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@f2pcatalog.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or (
        "admin1234" if FLASK_ENV == "development" else None
    )
