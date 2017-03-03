# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

from django.core.exceptions import ImproperlyConfigured
from .functions import get_env_variable


DATABASE_USER = get_env_variable('DATABASE_USER')
DATABASE_PASSWORD = get_env_variable('DATABASE_PASSWORD')
DATABASE_NAME = get_env_variable('DATABASE_NAME')
DATABASE_ENGINE = get_env_variable('DATABASE_ENGINE', default='django.db.backends.postgresql')
DATABASE_PORT = get_env_variable('DATABASE_PORT', default='5432')
DATABASE_HOST = get_env_variable('DATABASE_HOST', default='localhost')


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
