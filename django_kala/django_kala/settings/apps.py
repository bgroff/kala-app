INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',

    'auth.apps.AuthConfig',
    'organizations.apps.OrganizationsConfig',
    'documents.apps.DocumentsConfig',
    'django_kala',
    'projects.apps.ProjectsConfig',
]
