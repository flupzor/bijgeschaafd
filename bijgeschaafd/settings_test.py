import os

from .settings_base import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bijgeschaafd',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
    }
}

SECRET_KEY='BULLSHIT'
