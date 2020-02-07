"""
Django settings for ameribtc project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_REDIRECT_URL = '/index'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ftl$49mojhozrjk)ue7$1uq!-td)hn+qvrrp(6nod7#d**q*u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEV_SERVER = 'localhost'

# site domains
RAPLEV_URL = 'unstable-v.raplev.com'
AFFILIATES_URL = 'affiliates.raplev.com'
COMMUNITY_URL = 'community.raplev.com'
SCREENRECODER_URL = 'srecoder.raplev.com'

ALLOWED_HOSTS = [RAPLEV_URL, AFFILIATES_URL, COMMUNITY_URL, SCREENRECODER_URL, DEV_SERVER]
# for api server
HOSTNAME = 'http://unstable-v.raplev.com'

# Application definition

INSTALLED_APPS = [
    'cadmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',
    'theme',
    'rest_framework',
    'corsheaders',
    'apis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apis.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

CORS_ORIGIN_WHITELIST = [
    "http://" + COMMUNITY_URL,
    "http://" + AFFILIATES_URL,
]

ROOT_URLCONF = 'raplev.urls'

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
               'django.template.context_processors.media',
               'raplev.context_processors.global_settings',
               'cadmin.context_processors.cadmin_decorators',
               'theme.context_processors.theme_decorators',
           ],
       },
   },
]


WSGI_APPLICATION = 'raplev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ameribtc4',
        'USER': 'ameribtc3',
        'PASSWORD': 'Ameribtc3',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'cadmin.Users'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
  ('en', _('English')),
  ('ru', _('Русский')),
  ('io', _('Nigeria')),
  ('zh-hans', _('简体中文')),
]


# Add custom languages not provided by Django (io => ng)
import django.conf.locale
from django.conf import global_settings
global_settings.LANGUAGES = [(x[0], x[1]) if x[0] != 'io' else ('io', 'Nigeria') for x in global_settings.LANGUAGES]
django.conf.locale.LANG_INFO['io']['name'] = 'English'
django.conf.locale.LANG_INFO['io']['name_local'] = u'Nigeria'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/v-raplev/static'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'staic')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/v-raplev/media'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d', '%a %B %m %Y')
TIME_INPUT_FORMATS = ('%I:%M %p', '%H:%M:%S', '%H:%M')

# Email validation settings

EMAIL_CONFIRMATION_PERIOD_DAYS = 3
SIMPLE_EMAIL_CONFIRMATION_PERIOD = timedelta(days=EMAIL_CONFIRMATION_PERIOD_DAYS)
SIMPLE_EMAIL_CONFIRMATION_KEY_LENGTH = 16
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/opt/v-raplev/test_emails.txt'

TAGGIT_CASE_INSENSITIVE = True

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# Commento SSO settings
COMMENTO_HOST = 'commento.raplev.com'
#COMMENTO_HMAC_KEY = '5d79349b1dd90900c4132fe9b117f033e196c8f4b60b61b5ed0e41ceeaf8001d'
COMMENTO_HMAC_KEY = 'd260f51245e6efe3a6efc913b181dd2f72c482b6100a725603b82cdd8f1ec837'

# Google Maps API key
GOOGLE_API_KEY = 'AIzaSyDjN61hLnxRZJtMWWf_E-r7MThLVRPtgj0'
GOOGLE_GEOCODING_CACHE_TIME = 604800

# Twilio Settings
# Twilio Settings
TWILIO_ACCOUNT_SID = 'ACa7753e13018596d5193b423c8603f1c5'
TWILIO_AUTH_TOKEN = '3af418ebdd13244d2aff1dbbf225c30b'
TWILIO_VERIFICATION_SID = 'VA84385cf2852605f474a448127cba2488'
TWILIO_PHONE_NUMBER = '+15005550006'

FACEBOOK_LINK = 'https://www.facebook.com/'
LIKEDIN_LINK = 'https://www.linkedin.com/'
TWITTER_LINK = 'https://www.twitter.com/'
YOUTUBE_LINK = 'https://www.youtube.com/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(process)-5d %(thread)d %(name)-50s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
         'level': 'INFO',
         'class': 'logging.handlers.SysLogHandler',
         'facility': 'local7',
         'address': '/dev/log',
         'formatter': 'verbose'
       },
    },
    'loggers': {
        # root logger
        '':{
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'disabled': False
        },
        'thingsforwork': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
