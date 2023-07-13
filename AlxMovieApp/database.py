from pathlib import Path
from dotenv import load_dotenv
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

POSTGRES = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'movie_app',
    'USER': 'django',
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'OPTIONS': {
    },
}
# SQLITE = {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': BASE_DIR / 'db.sqlite3',
# }

DB_CONFIG = {
    'default': POSTGRES,
}
