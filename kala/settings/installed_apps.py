from kala.settings import get_env_variable


DEPLOYMENT_ENVIRONMENT = get_env_variable('KALA_DEPLOYMENT_ENVIRONMENT')

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'ndptc.accounts',

    'accounts',
    'companies',
    'documents',
    'kala',
    'projects',

)


if DEPLOYMENT_ENVIRONMENT is 'development':
    INSTALLED_APPS += ('debug_toolbar',)
