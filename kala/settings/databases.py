from django.core.exceptions import ImproperlyConfigured
from kala.settings.functions import get_env_variable


DATABASE_USER = get_env_variable('KALA_DATABASE_USER')
DATABASE_PASSWORD = get_env_variable('KALA_DATABASE_PASSWORD')

try:
    DATABASE_ENGINE = get_env_variable('KALA_DATABASE_ENGINE')
except ImproperlyConfigured:
    DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'

try:
    DATABASE_NAME = get_env_variable('KALA_DATABASE_NAME')
except ImproperlyConfigured:
    DATABASE_NAME = 'ndptc'

try:
    DATABASE_PORT = get_env_variable('KALA_DATABASE_PORT')
except ImproperlyConfigured:
    DATABASE_PORT = '5432'

try:
    DATABASE_HOST = get_env_variable('KALA_DATABASE_HOST')
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
