from django_kala.functions import get_env_variable

AVATAR_BASE_PATH = get_env_variable('AVATAR_BASE_PATH', '/tmp/avatars')
AVATAR_BASE_URL = get_env_variable('AVATAR_BASE_URL', 'http://localhost:9090/media/avatars')
EXPORT_BASE_PATH = get_env_variable('EXPORT_BASE_PATH', '/tmp/exports')
EXPORT_BASE_URL = get_env_variable('EXPORT_BASE_URL', 'http://localhost:9090/media/exports')
DOCUMENT_BASE_PATH = get_env_variable('DOCUMENT_BASE_PATH', '/tmp/documents')
DOCUMENT_BASE_URL = get_env_variable('DOCUMENT_BASE_URL', 'http://localhost:9090/media/documents')

CELERY_BROKER_USER = get_env_variable('CELERY_BROKER_USER', 'kala')
CELERY_BROKER_PASSWORD = get_env_variable('CELERY_BROKER_PASSWORD', 'kala')
CELERY_BROKER_HOST = get_env_variable('CELERY_BROKER_HOST', 'localhost:5672')
CELERY_BROKER_VHOST = get_env_variable('CELERY_BROKER_VHOST', '')

CELERY_BROKER_URL = 'amqp://{0}:{1}@{2}/{3}'.format(
    CELERY_BROKER_USER,
    CELERY_BROKER_PASSWORD,
    CELERY_BROKER_HOST,
    CELERY_BROKER_VHOST
)
