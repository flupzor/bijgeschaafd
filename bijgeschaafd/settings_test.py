import os

from settings_base import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.dirname(APP_ROOT)+'/newsdiffs.db',
    }
}

SECRET_KEY='BULLSHIT'
