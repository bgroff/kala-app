import os
from django.core.exceptions import ImproperlyConfigured
from kala.settings.databases import DATABASES
from kala.settings.functions import get_env_variable
from kala.settings.installed_apps import INSTALLED_APPS


ALLOWED_HOSTS = ('localhost', 'kala.ndptc.manoa.hawaii.edu',)
if get_env_variable('KALA_DEPLOYMENT_ENVIRONMENT') is 'development':
    # IP Address used by vagrant
    ALLOWED_HOSTS += ('10.1.1.10',)
DEBUG = True

AUTH_USER_MODEL = 'accounts.Person'

AUTHENTICATION_BACKENDS = (
    'ndptc.accounts.backends.UHBackend',
    'django.contrib.auth.backends.ModelBackend',
)

INTERNAL_IPS = ('127.0.0.1',)

try:
    LANGUAGE_CODE = get_env_variable('KALA_LANGUAGE_CODE')
except ImproperlyConfigured:
    LANGUAGE_CODE = 'en-us'

LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'
MEDIA_URL = '/media/'
ROOT_URLCONF = 'moi.urls'
SECRET_KEY = get_env_variable('KALA_SECRET_KEY')
STATIC_URL = '/static/'

try:
    TIME_ZONE = get_env_variable('KALA_TIME_ZONE')
except ImproperlyConfigured:
    TIME_ZONE = 'Pacific/Honolulu'

USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'moi.wsgi.application'

SITE_ROOT = os.path.realpath(os.path.dirname(__file__) + '../')
DOCUMENT_ROOT = os.path.join(SITE_ROOT, 'documents/')
DATA_ROOT = os.path.join(SITE_ROOT, 'data/')
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
