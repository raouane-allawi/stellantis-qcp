from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

USE_FAKE_API = True
# Emails print to terminal during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'