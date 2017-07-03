AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT = '/'
