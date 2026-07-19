import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nexzone-universidad-2026-segura"
    JWT_SECRET = os.environ.get("JWT_SECRET") or "nexzone_jwt_secret_universidad_2026"
    DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    TEMPLATES_AUTO_RELOAD = True

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DB = os.environ.get("MYSQL_DB", "nexzone_db")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
