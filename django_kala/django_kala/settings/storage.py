from .debug import DEBUG


if not DEBUG:
    DEFAULT_FILE_STORAGE = 'django_kala.storage.MediaStorage'

EXPORT_EXPIRATION_IN_DAYS=5
