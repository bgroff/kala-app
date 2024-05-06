from django_kala.functions import get_env_variable

# Django settings
EMAIL_BACKEND = get_env_variable('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = get_env_variable('EMAIL_HOST', 'localhost')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', default='')
EMAIL_PORT = get_env_variable('EMAIL_PORT', default=25)
EMAIL_SUBJECT_PREFIX = get_env_variable('EMAIL_SUBJECT_PREFIX', default='')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', default=False)
EMAIL_USE_SSL = get_env_variable('EMAIL_USE_SSL', default=False)
EMAIL_SSL_CERTFILE = get_env_variable('EMAIL_SSL_CERTFILE', default=False)
EMAIL_SSL_KEYFILE = get_env_variable('EMAIL_SSL_KEYFILE', default=False)
EMAIL_TIMEOUT = get_env_variable('EMAIL_TIMEOUT', default=False)

# Kala settings
FROM_EMAIL = get_env_variable('FROM_EMAIL', default='kala@maloloindustries.com')
HELP_EMAIL = get_env_variable('HELP_EMAIL', default='help')
EMAIL_APP = get_env_variable('EMAIL_APP', default='kala') # Use this to customize the email templates.
USE_HTML_EMAIL = get_env_variable('USE_HTML_EMAIL', default=False)
