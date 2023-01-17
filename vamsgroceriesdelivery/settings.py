"""
Django settings for vamsgroceriesdelivery project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
if DEBUG == True:
    admin_volt = 'admin_volt.apps.AdminVoltConfig'

# Application definition

INSTALLED_APPS = [
    # admin_volt,
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #account App
    'user.apps.AccountConfig',

    #products APP
    'products.apps.ProductsConfig',

    #store App
    'stores.apps.StoresConfig',

    #cart app
    'cart.apps.CartConfig',

    #Third-party App
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',  # new
    'allauth.account',  # new
    'allauth.socialaccount',  # new
    'dj_rest_auth.registration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vamsgroceriesdelivery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
SITE_ID = 1

WSGI_APPLICATION = 'vamsgroceriesdelivery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "gdeliveryproject2",
            "USER": "postgres",
            "PASSWORD": "Shekhar123#",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('USERNAME'),
            'PASSWORD': env('PASSWORD'),
            'HOST': env('DATABASE_URL'),
            'PORT': env('DATABASE_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT =  os.path.join(BASE_DIR ,'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [ # new
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

AUTH_USER_MODEL = env.str('AUTH_USER_MODEL')
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'user.serializers.LoginSerializer'
}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializers.RegisterSerializer'
}
ACCOUNT_AUTHENTICATION_METHOD=env('ACCOUNT_AUTHENTICATION_METHOD')
ACCOUNT_USERNAME_REQUIRED=env('ACCOUNT_USERNAME_REQUIRED')
ACCOUNT_EMAIL_REQUIRED=env('ACCOUNT_EMAIL_REQUIRED')
ACCOUNT_UNIQUE_EMAIL=env('ACCOUNT_UNIQUE_EMAIL')
ACCOUNT_EMAIL_VERIFICATION=env('ACCOUNT_EMAIL_VERIFICATION')
ACCOUNT_ADAPTER = 'user.adapters.CustomUserAccountAdapter'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#INSTAMOJO API DETAILS
API_KEY = env('INSTAMOJO_API_KEY')
AUTH_TOKEN = env('INSTAMOJO_AUTH_TOKEN')
API_SALT = env('INSTAMOJO_API_SALT')
PAYMENT_SUCCESS_REDIRECT_URL = env('PAYMENT_SUCCESS_REDIRECT_URL')
SEND_SMS=env('INSTAMOJO_SEND_PAYMENT_RECEIVED_SMS')
SEND_EMAIL=env('INSTAMOJO_SEND_PAYMENT_RECEIVED_EMAIL')
ENDPOINT = env('INSTAMOJO_TEST_ENDPOINT')