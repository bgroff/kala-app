from django.conf import settings

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
