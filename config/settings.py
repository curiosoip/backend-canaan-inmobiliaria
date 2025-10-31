from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-!-fs-ay&5!5r&!#ona1t-xl5p#hiv7_l-1bmp(%+y(2h4rdp7@'

DEBUG = True

ALLOWED_HOSTS = [
    "canaan-inmobiliaria-admin.up.railway.app",
    "web-inmobiliaria-canaan.pages.dev",
    "localhost",
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'corsheaders',             
    'compressor',
    'apps.procesos',
    'apps.departamentos',
    'apps.reportes',
    'apps.urbanizaciones',
    'apps.contabilidad',
    'apps.usuarios',
    'apps.ventas',
    'apps.cuotas',
    'apps.pagos',
    'apps.servicios',
    'apps.viviendas',
    'apps.perfiles',
    'apps.tramites',
    'apps.mensajes',
    'apps.web',
]



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:4321",
    "http://localhost:4322",
    "https://web-inmobiliaria-canaan.pages.dev",
    "https://canaan-inmobiliaria-admin.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:4321",
    "http://localhost:4322",
    "https://web-inmobiliaria-canaan.pages.dev",
    "https://canaan-inmobiliaria-admin.up.railway.app",
]


CSRF_COOKIE_HTTPONLY = False  
CSRF_COOKIE_SECURE = False   
CSRF_USE_SESSIONS = False  
CSRF_COOKIE_SECURE = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

LOGIN_URL = 'login'  
LOGOUT_REDIRECT_URL = 'login'  
AUTH_USER_MODEL = 'usuarios.Usuario'

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,  
        ssl_require=True, 
    )
}

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

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"

'''
STATICFILES_DIRS = [
    BASE_DIR / "static",  
]
'''

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
