import os
from pathlib import Path

try:
    import environ
except ImportError:  # pragma: no cover - local fallback when django-environ is missing
    environ = None

BASE_DIR = Path(__file__).resolve().parent.parent


class _SimpleEnv:
    @staticmethod
    def read_env(path):
        with open(path, "r", encoding="utf-8") as env_file:
            for raw_line in env_file:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

    @staticmethod
    def str(key, default=None):
        value = os.environ.get(key, default)
        if value is None:
            raise RuntimeError(f"Environment variable '{key}' is required")
        return value

    @staticmethod
    def bool(key, default=False):
        value = os.environ.get(key)
        if value is None:
            return default
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def list(key, default=None):
        value = os.environ.get(key)
        if value is None:
            return list(default or [])
        return [item.strip() for item in value.split(",") if item.strip()]


env = environ.Env() if environ else _SimpleEnv()

env_path = BASE_DIR / ".env"
if not env_path.exists():
    env_path = BASE_DIR.parent / ".env"

if env_path.exists():
    if environ:
        environ.Env.read_env(str(env_path))
    else:
        env.read_env(env_path)

# DJANGO CORE SETTINGS
DJANGO_SETTINGS_MODULE = env.str("DJANGO_SETTINGS_MODULE", default="core.settings.dev")
SECRET_KEY = env.str("SECRET_KEY", default="unsafe-secret-key")
DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# DATABASE SETTINGS
DB_ENGINE = env.str("DB_ENGINE", default="django.db.backends.sqlite3")
DB_NAME = env.str("DB_NAME", default=str(BASE_DIR / "db.sqlite3"))
DB_USER = env.str("DB_USER", default="")
DB_PASSWORD = env.str("DB_PASSWORD", default="")
DB_HOST = env.str("DB_HOST", default="")
DB_PORT = env.str("DB_PORT", default="")
DB_SSLMODE = env.str("DB_SSLMODE", default="prefer")

# Telegram bot
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_CHANNEL_ID = env.str("TELEGRAM_CHANNEL_ID", default="")
