# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/
from django_kala.functions import import_from_string

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'taggit',

    'auth.apps.AuthConfig',
    'organizations.apps.OrganizationsConfig',
    'documents.apps.DocumentsConfig',
    'django_kala',
    'projects.apps.ProjectsConfig',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
AUTH_USER_MODEL = 'kala_auth.User'
ACCOUNT_ACTIVATION_DAYS = 15
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
USE_CERTIFICATES = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


ALLOWED_HOSTS = ['localhost']

ROOT_URLCONF = 'django_kala.urls'
STATIC_URL = '/static/'
LANGUAGE_CODE = 'en-us'
SECRET_KEY = 'foobar'
DOCUMENT_ROOT = ''
import os
STATIC_ROOT = os.path.join(os.path.dirname(__file__) + '/..', 'static/')
MEDIA_ROOT = '/tmp'

TIME_ZONE = 'Pacific/Honolulu'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'

PLATFORM_MANAGER = import_from_string(
    'django_kala.platforms.test.manager.PlatformManager',
    'PLATFORM_MANAGER'
)

EXPORT_QUEUE = 'test'
CELERY_BROKER_URL = 'memory://'
EMAIL_APP = 'kala'
USE_HTML_EMAIL = False
APPLICATION_URL = 'http://localhost'
HELP_EMAIL = 'test.help'
FROM_EMAIL = 'test.help@test'
EXPORT_DIRECTORY = '/tmp/test_exports/'
