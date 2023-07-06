from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# MYSQL = {
#     'ENGINE': 'django.db.backends.mysql',  # 'django.db.backends.mysql',
#     'NAME': 'movie_app',
#     'HOST': '127.0.0.1',
#     'USER': 'root',
#     'PASSWORD': 'm!s3rv3r',
#     'OPTIONS': {
#         'charset': 'utf8mb4',
#         'use_unicode': True,
#     },
# }
# POSTGRES = {
#     'ENGINE': 'django.db.backends.',
#     'NAME': 'movie_app',
#     'USER': 'django',
#     'PASSWORD': 'e2a78aa641d7519a96e99040aa21a2bb',
#     'OPTIONS': {
#     },
# }
SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

DB_CONFIG = {
    'default': SQLITE,
}
