from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "the_manor",
        "USER": "macy",
        "PASSWORD": "1234",
        # "HOST": os.getenv("DB_HOST"),
        # "PORT": os.getenv("DB_PORT"),
    }
}
