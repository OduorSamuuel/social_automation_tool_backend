import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-8%p)f2bg^u%$7g^$e3o9#k)n_pwhl^e%ib*19g)&%rbni$13s@')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]

# CSRF configuration
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
]

CORS_ALLOW_CREDENTIALS = True  # Make sure this is set to allow cookies

# Application definition
INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'social_django',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'rest_framework',
    'djoser',
    'core',
    'accounts',
     'social', 
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Should be first to handle CORS preflight requests
    'django.middleware.security.SecurityMiddleware',  # Handles security measures like HTTPS
    'django.contrib.sessions.middleware.SessionMiddleware',  # Ensures session data is available early
    'django.middleware.common.CommonMiddleware',  # Common tasks like handling response headers
    'django.middleware.csrf.CsrfViewMiddleware',  # Handles CSRF protection, which requires session to be set first
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Uses session to authenticate users
    'django.contrib.messages.middleware.MessageMiddleware',  # Provides messaging framework (depends on session)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protects against clickjacking
    'allauth.account.middleware.AccountMiddleware',  # Handles account-specific logic
]

FACEBOOK_CLIENT_ID = '1926414434547076'
FACEBOOK_CLIENT_SECRET = 'a78d8358ae882a8aa10d198f08e00091'
FACEBOOK_REDIRECT_URI = 'http://localhost:8000/api/social/facebook/callback/'

# Google OAuth2 configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', '161841218791-6rgpmnm1inblhi5bk0gvvntn0ulku4mr.apps.googleusercontent.com'),
            'secret': os.environ.get('GOOGLE_CLIENT_SECRET', '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'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Update to point to the 'core' app for routing
ROOT_URLCONF = 'core.urls'

AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
   # 'social_core.backends.google.GoogleOAuth2',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Update to point to the 'core' app for WSGI
WSGI_APPLICATION = 'core.wsgi.application'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'onyangos949@gmail.com')  # Use environment variable for security
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'uyryzvssxrinfivg')  # Use environment variable for security
DEFAULT_FROM_EMAIL = 'Onyangos Team <onyangos949@gmail.com>'

# Database configuration (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'django-saas'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '813456'),
        'HOST': 'localhost',  # For production, update this
        'PORT': '5432',       # PostgreSQL default port
    }
}

# REST framework and JWT setup
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # Optional: if you want to allow basic auth as well
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # Comment out if you don't want JWT
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Configure JWT lifespan and settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Optional: define where to look for additional static files
# STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
GOOGLE_CLIENT_ID='161841218791-6rgpmnm1inblhi5bk0gvvntn0ulku4mr.apps.googleusercontent.com'

# Logging configuration (optional)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
