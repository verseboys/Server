# this file is used for running 'manage.py collectstatic only'

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace("\\", "/")

# the value of secret_key is not important, collectstatic does not need it,
# but requires it not to be empty.
# > django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
SECRET_KEY = 'abcdefg'

# we need INSTALLED_APPS to make 'collectstatic' working
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api.front',
    'api.supervisor',
    'api.webapp_front',
    'articlemodel',
    'frontmodel',
    'supervisormodel',
    'extends',
    'questionsandanswersmodel',
    'methodmodel',
    'newsmodel',
    'videomodel',
    'djcelery',
    'anniversary',
    'models',
]
