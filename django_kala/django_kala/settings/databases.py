# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

from django.core.exceptions import ImproperlyConfigured
from .functions import get_env_variable


DATABASE_USER = get_env_variable('DATABASE_USER')
DATABASE_PASSWORD = get_env_variable('DATABASE_PASSWORD')
DATABASE_NAME = get_env_variable('DATABASE_NAME')

try:
    DATABASE_ENGINE = get_env_variable('DATABASE_ENGINE')
except ImproperlyConfigured:
    DATABASE_ENGINE = 'django.db.backends.postgresql'

try:
    DATABASE_PORT = get_env_variable('DATABASE_PORT')
except ImproperlyConfigured:
    DATABASE_PORT = '5432'

try:
    DATABASE_HOST = get_env_variable('DATABASE_HOST')
except ImproperlyConfigured:
    DATABASE_HOST = 'localhost'


DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}
