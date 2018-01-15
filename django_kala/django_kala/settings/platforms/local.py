from django_kala.settings import get_env_variable

AVATAR_BASE_URL = get_env_variable('AVATAR_BASE_URL', 'http://localhost:9090/media/avatar/')
EXPORT_DIRECTORY = get_env_variable('EXPORT_DIRECTORY', '/tmp/exports/')
