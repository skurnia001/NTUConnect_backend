"""
Django settings for NTUConnect_backend project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from datetime import timedelta
from enum import Enum
from pathlib import Path


class DeployPhaseEnum(Enum):
    LOCAL = 1
    STAGING = 2
    PROD = 3
    TEST = 5


# Deploy phase
deploy_phase = os.getenv('DEPLOY_PHASE', 'LOCAL')

if deploy_phase == 'PROD':
    deploy_phase = DeployPhaseEnum.PROD
elif deploy_phase == 'STAGING':
    deploy_phase = DeployPhaseEnum.STAGING
elif deploy_phase == 'TEST':
    deploy_phase = DeployPhaseEnum.TEST
else:
    deploy_phase = DeployPhaseEnum.LOCAL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'rvy(8cms9+(%c!#p23^*bvlv6q67(#pxc3t6b!a(zp+$a+qk_0')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Local
    'APIServer.apps.ApiserverConfig',

    # 3rd party
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'django_s3_storage',
    'corsheaders'
]

if deploy_phase == DeployPhaseEnum.PROD:
    YOUR_S3_BUCKET = "zappa-static-ntuconnect"

    STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET

    # These next two lines will serve the static files directly
    # from the s3 bucket
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
else:
    STATIC_URL = '/static/'

AUTH_USER_MODEL = 'APIServer.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'EXCEPTION_HANDLER': 'APIServer.exceptions.custom_exception_handler',
}

REST_USE_JWT = True

JWT_AUTH_COOKIE = 'JWT'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

if deploy_phase == DeployPhaseEnum.LOCAL:
    # CSRF SETTINGS
    CSRF_COOKIE_SECURE = False

    SESSION_COOKIE_SECURE = False

    SECURE_SSL_REDIRECT = False
else:
    # CSRF SETTINGS
    CSRF_COOKIE_SECURE = True

    SESSION_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True

ROOT_URLCONF = 'NTUConnect_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
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

WSGI_APPLICATION = 'NTUConnect_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if deploy_phase == DeployPhaseEnum.PROD:
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': os.getenv('DATABASE_NAME', 'NTUConnectDB'),
            'CLIENT': {
                'username': os.getenv('DATABASE_UNAME'),
                'password': os.getenv('DATABASE_PWD'),
                'host': os.getenv('DATABASE_HOST'),
                'authSource': 'admin',
            }
        }
    }
elif deploy_phase == DeployPhaseEnum.LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True
