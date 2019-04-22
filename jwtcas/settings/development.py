from .base import *

DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'


MEDIA_URL = '/media/'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cas',
        'USER': 'cas',
        'PASSWORD': 'cas',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}