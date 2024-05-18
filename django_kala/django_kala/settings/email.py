from django_kala.functions import get_env_variable

# Django settings
EMAIL_BACKEND = get_env_variable('KALA_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_env_variable('KALA_EMAIL_HOST', 'localhost')
EMAIL_HOST_PASSWORD = get_env_variable('KALA_EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = get_env_variable('KALA_EMAIL_HOST_USER', default='')
EMAIL_PORT = get_env_variable('KALA_EMAIL_PORT', default=25)
EMAIL_SUBJECT_PREFIX = get_env_variable('KALA_EMAIL_SUBJECT_PREFIX', default='')
EMAIL_USE_TLS = bool(get_env_variable('KALA_EMAIL_USE_TLS', default=False))
EMAIL_USE_SSL = bool(get_env_variable('KALA_EMAIL_USE_SSL', default=False))
EMAIL_SSL_CERTFILE = get_env_variable('KALA_EMAIL_SSL_CERTFILE', default=False)
EMAIL_SSL_KEYFILE = get_env_variable('KALA_EMAIL_SSL_KEYFILE', default=False)

timeout = get_env_variable('KALA_EMAIL_TIMEOUT', default=None)
EMAIL_TIMEOUT = int(timeout) if timeout is not None else None

# Kala settings
FROM_EMAIL = get_env_variable('KALA_FROM_EMAIL', default='kala@maloloindustries.com')
HELP_EMAIL = get_env_variable('KALA_HELP_EMAIL', default='help')
EMAIL_APP = get_env_variable('KALA_EMAIL_APP', default='kala') # Use this to customize the email templates.
USE_HTML_EMAIL = get_env_variable('KALA_USE_HTML_EMAIL', default=False)
