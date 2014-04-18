import os
if os.environ['DJANGO_SETTINGS_MODULE'] != 'runtests':
    from django.core.exceptions import ImproperlyConfigured
    from .databases import DATABASES
    from .functions import get_env_variable
    from .installed_apps import INSTALLED_APPS


    ALLOWED_HOSTS = ('localhost', 'kala.localhost',)
    if get_env_variable('KALA_DEPLOYMENT_ENVIRONMENT') == 'development':
        # IP Address used by vagrant
        ALLOWED_HOSTS += ('10.1.1.10',)
    DEBUG = True

    AUTH_USER_MODEL = 'accounts.Person'

    AUTHENTICATION_BACKENDS = (
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
    ROOT_URLCONF = 'kala.urls'
    SECRET_KEY = get_env_variable('KALA_SECRET_KEY')
    STATIC_URL = '/static/'

    try:
        TIME_ZONE = get_env_variable('KALA_TIME_ZONE')
    except ImproperlyConfigured:
        TIME_ZONE = 'Pacific/Honolulu'

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WSGI_APPLICATION = 'kala.wsgi.application'

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__) + '/..')
    if get_env_variable('KALA_DEPLOYMENT_ENVIRONMENT') == 'development':
        DOCUMENT_ROOT = '/tmp/'
    else:
        DOCUMENT_ROOT = os.path.join(SITE_ROOT, 'documents/')
    DATA_ROOT = os.path.join(SITE_ROOT, 'data/')
    MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')
    STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.core.context_processors.request",
        "django.contrib.messages.context_processors.messages"
    )
