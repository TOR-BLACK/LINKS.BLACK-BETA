import os
from pathlib import Path

# region CONSTANTS
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSPORT = os.getenv('REDIS_PASSPORT', '')
# endregion

# region DJANGO CORE SETTINGS
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://localhost').split(' ')
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

DJANGO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
APPS = [
    'apps.users',
    'apps.dv_info_site'
]
LIBS = [
    'corsheaders',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'modeltranslation',
    'markdownx',
]
INSTALLED_APPS = DJANGO + LIBS + APPS
WSGI_APPLICATION = 'core.wsgi.application'
ROOT_URLCONF = 'core.urls'

MAIN_ADMIN_URL = os.getenv('MAIN_ADMIN_URL', 'https://localhost')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'core.jwt_middleware.JWTAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'core.middleware.language_middleware.LanguageLogMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# region INTERNATIONALIZATION
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('zh', '中文'),
    ('pt', 'Português'),
    ('es', 'Español'),
    ('hi', 'हिंदी'),
    ('ar', 'العربية'),
    ('kk', 'Қазақша'),
    ('hy', 'Հայերեն'),
    ('az', 'Azərbaycan'),
    ('ro', 'Română'),
    ('uk', 'Український'),
    ('ky', 'Кыргыз тили'),
    ('uz', 'O’zbek'),
    ('tg', 'Тоҷикӣ'),
    ('tr', 'Türk')
]
#LANGUAGE_CODE = '-'.join([x[0] for x in LANGUAGES])
LANGUAGE_CODE = 'ru'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'  # Язык по умолчанию
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'ru')  # Порядок фоллбэка

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# endregion


# endregion


# region DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{REDIS_PASSPORT}@{REDIS_HOST}:{REDIS_PORT}/1',
    }
}
USER_PERMISSION_CACHE_KEY = 'user_{user_id}_permissions'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# endregion

# region LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose'
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'apps.dv_info_site.services.product_parsing': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core.celery': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
# endregion

# region LIBS SETTINGS

# region REST_FRAMEWORK_SETTINGS
SWAGGER_API_URL = os.getenv('SWAGGER_API_URL', 'https://localhost')
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}
    },
    'DEFAULT_MODEL_RENDERING': 'example'

}
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'api.da_vinci_info_site.renderers.MultiLanguageJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

AUTH_JWT_SECRET = os.getenv('AUTH_JWT_SECRET')
AUTH_JWT_ALGORITHMS = os.getenv('AUTH_JWT_ALGORITHMS', "HS256").split(',')
# endregion


# region CORS headers
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# endregion


# endregion


# region SERVICES
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

GOOGLE_OAUTH2_CREDENTIALS = {
    "type": os.getenv("GOOGLE_OAUTH2_TYPE"),
    "project_id": os.getenv("GOOGLE_OAUTH2_PROJECT_ID"),
    "private_key_id": os.getenv("GOOGLE_OAUTH2_PRIVATE_KEY_ID"),
    "private_key": os.getenv("GOOGLE_OAUTH2_PRIVATE_KEY"),  # Замена для корректного формата
    "client_email": os.getenv("GOOGLE_OAUTH2_CLIENT_EMAIL"),
    "client_id": os.getenv("GOOGLE_OAUTH2_CLIENT_ID"),
    "auth_uri": os.getenv("GOOGLE_OAUTH2_AUTH_URI"),
    "token_uri": os.getenv("GOOGLE_OAUTH2_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("GOOGLE_OAUTH2_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("GOOGLE_OAUTH2_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("GOOGLE_OAUTH2_UNIVERSE_DOMAIN")
}
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
# endregion


# region CELERY
CELERY_BROKER_URL = f'redis://:{REDIS_PASSPORT}@{REDIS_HOST}:{REDIS_PORT}/2'
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BROKER_TRANSPORT = 'redis'
CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSPORT}@{REDIS_HOST}:{REDIS_PORT}/2'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# endregion

DVI_CLIENT_AUTH = {
    'LOGIN': os.getenv('DVI_CLIENT_LOGIN'),
    'PASSWORD': os.getenv('DVI_CLIENT_PASSWORD'),
}
