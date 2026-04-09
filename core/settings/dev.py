from core import config
from core.log_config import get_logging_config
from .base import *

# Development logging
LOGGING = get_logging_config(environment='development')

# Show SQL queries in console (optional)
LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'

DEBUG = True
SECRET_KEY = config.SECRET_KEY
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# Local DB directly via psycopg2
DATABASE_ENGINE = config.DB_ENGINE

if DATABASE_ENGINE.endswith('sqlite3'):
    db_name = config.DB_NAME or (BASE_DIR / 'db.sqlite3')
else:
    db_name = config.DB_NAME

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': db_name,
        'USER': config.DB_USER,
        'PASSWORD': config.DB_PASSWORD,
        'HOST': config.DB_HOST,
        'PORT': config.DB_PORT,
    }
}

# Optional: local-specific logging or debug toolbar
INSTALLED_APPS += [
    # 'debug_toolbar',
]
