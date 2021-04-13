"""
Django settings for CTAFramework project.

Generated by "django-admin startproject" using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

# Checks environment mode
if not os.environ.get("ENV_FILE"):
    error_msg = "ENV_FILE not defined, did you load the correct .env file?"
    raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG")))

# Settings for production environment
if DEBUG == False:
    SESSION_COOKIE_SECURE = bool(int(os.environ.get("SESSION_COOKIE_SECURE")))
    SECURE_SSL_REDIRECT = bool(int(os.environ.get("SECURE_SSL_REDIRECT")))
    CSRF_COOKIE_SECURE = bool(int(os.environ.get("CSRF_COOKIE_SECURE")))
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS"))

COMPRESS_OFFLINE = bool(int(os.environ.get("COMPRESS_OFFLINE")))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(",")
print(ALLOWED_HOSTS)

X_FRAME_OPTIONS = "SAMEORIGIN"

# Application definition
CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
#    "rest_framework_docs",
    "django_filters",
    "compressor",
    "rolepermissions"
]

PROJECT_APPS = [
    "apps.apis",
    "apps.Products",
    "apps.Servers",
    "apps.Testings",
    "apps.Users",
]

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "CTAFramework.urls"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "CTAFramework.context_processors.sitewide"
            ],
        },
    },
]

WSGI_APPLICATION = "CTAFramework.wsgi.application"

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": int(os.environ.get("DB_PORT")),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)

STATIC_ROOT = "/var/www/static/"
STATIC_URL = "/static/"

COMPRESS_ENABLED = DEBUG
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT

MEDIA_ROOT = "/var/www/media"
MEDIA_URL = "media/"

AUTH_USER_MODEL = "Users.User"

ADMIN_MAIL = os.environ.get("ADMIN_MAIL")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "TestSite Team <{}>".format(os.environ.get("EMAIL_HOST_USER"))

SITE_DNS = os.environ.get("SITE_DNS")

# Flag for use BluePage Auth
IBM_CLIENT = int(os.environ.get("IBM_CLIENT"))
# Flag for use UTF-8 on extract  (Disable improve the speed)
DEPTH_SEARCH = int(os.environ.get("DEPTH_SEARCH"))

PLATFORM_VERSION = os.environ.get("PLATFORM_VERSION")

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),
}

CELERY_APP_NAME = os.environ.get("CELERY_APP_NAME")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_BROKER_POOL_LIMIT = None
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

ROLEPERMISSIONS_MODULE = "CTAFramework.roles"
ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True

CTA_MAN_COMMAND = "man -L en"