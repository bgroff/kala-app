from django_kala.functions import get_env_variable

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: This should be less strange.
deployment = get_env_variable('DEPLOYMENT', True)
if type(deployment) is str:
    if deployment == 'production':
        DEBUG = False
    else:
        DEBUG = True
        from .apps import INSTALLED_APPS
        from .middleware import MIDDLEWARE
#        INSTALLED_APPS += ['debug_toolbar']
#        MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
        INTERNAL_IPS = ['10.0.2.2']
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
