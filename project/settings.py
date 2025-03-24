"""
Django settings for project project.

"""
import os
import sys
from distutils.util import strtobool
from pathlib import Path
from dotenv import dotenv_values
from datetime import timedelta 
import sentry_sdk
from django.utils.log import DEFAULT_LOGGING

from sentry_sdk.integrations.django import DjangoIntegration

config = dotenv_values(".env.uat")

for key, value in config.items():
    os.environ[key] = value

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = 'Um2ga1-#2secret#p!ezs0^!^o#0'
TIME_ZONE = 'Asia/Kolkata'

# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE")


# Application definition
INSTALLED_APPS = [
    'ramailo.apps.RamailoConfig',
    'rest_framework',
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework_simplejwt',
    'django_extensions',
    'user',
    'stock',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'project.middleware.UserLoggingMiddleware'
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', default='ramailo_dev'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST', default='127.0.0.1'),
        'PORT': int(os.environ.get('POSTGRES_PORT', default=5432)),

    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', default='redis://localhost:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE = "default"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATICFILES_DIRS = (('static'),)
STATIC_URL = os.environ.get('STATIC_URL', default='static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', default='static'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'EXCEPTION_HANDLER': 'ramailo.error_handling.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Changed to this
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    "ALGORITHM": "HS512",
    'SIGNING_KEY': os.environ.get("JWT_SIGNING_KEY"),
    'AUTH_HEADER_TYPES': ("Bearer",),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    "VERIFYING_KEY": "",
    "JTI_CLAIM": None,
    "USER_ID_CLAIM": "id"
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'USE_SESSION_AUTH': False
}

# CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', default=False)
# SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', default=False)
ENV_ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = ENV_ALLOWED_HOSTS.split(',') if ENV_ALLOWED_HOSTS is not None else []
DEBUG = bool(strtobool(os.environ.get('DEBUG', default='True')))

# Ramailo
COMPANY_NAME = "Ramailo"

# User
DUMMY_USER_IMAGE = 'https://ramailo-logos.s3.ap-south-1.amazonaws.com/misc/dummy_user.png'

# Email
EMAIL_OTP_EXPIRY = 5 * 60
EMAIL_LINK_EXPIRY = 5 * 60
EMAIL_REQUEST_RATE_LIMIT = '3/5m' # 3 requests in 5 min

# App URL
APP_URL = os.getenv("APP_URL")
WEB_URL = os.getenv("WEB_URL")

# Subscription
AUTO_EXPIRES_ON=3650 # days

#sentry
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)

#loggers
LOGGING = {
    # Define the logging version
    'version': 1,

    # Enable the existing loggers
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'user_idx': {
            '()': 'shared.helpers.logging_helper.UserIDXFilter'
        },
    },

    # Define the formatters
    'formatters': {
            'verbose': {
            'format': '[%(levelname)s] [%(asctime)s] [%(module)s] [%(lineno)s] [%(user_idx)s] [%(message)s] ',
            },
    },

    # Define the handlers
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['user_idx'],
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['user_idx'],
            'filename': 'logs.log',
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },

   # Define the loggers
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },

        #database query logger
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        # }
    },

}

#celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_ACCEPTY_CONTENT= ["json"]
CELERY_TASK_SERIALIZER = "json"
CLERY_RESULT_SERIALIZER = 'json'


## Email Configuraton
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT='587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD= os.environ.get("EMAIL_HOST_PASSWORD")

CSRF_TRUSTED_ORIGINS = ["https://ramailo.uat.ramailo.tech"]

##ALPHA_VANTAGE_API_KEY
ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE")

#refer
REFERRAL_URL = os.environ.get("REFERRAL_URL")

#razorpay-ifsc
RAZORPAY_IFSC_URL=os.environ.get("RAZORPAY_IFSC_URL")


#s3 configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' 

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True

# aws ses
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME")
# AWS_SES_EMAIL = os.environ.get("AWS_SES_EMAIL")

#fcm
FCM_API_KEY = os.environ.get("FCM_API_KEY")

# testers
TESTERS = ["9975319000", "8864208000"]

# Name matching threshold
NAME_MATCH_THRESHOLD = 70.0


# some of the available stocks
AVAILABLE_STOCKS = [
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "AMZN", "name": "Amazon.com Inc."},
    {"symbol": "TSLA", "name": "Tesla Inc."},
]