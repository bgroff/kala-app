from django_kala.functions import get_env_variable

endpoint = get_env_variable('KALA_STORAGE_ENDPOINT', 'http://minio:9000')
if endpoint != '':
    KALA_STORAGE_ENDPOINT = endpoint
else:
    KALA_STORAGE_ENDPOINT = None

KALA_STORAGE_BUCKET = get_env_variable('KALA_STORAGE_BUCKET', 'kala-docs')
KALA_STORAGE_PREFIX = get_env_variable('KALA_STORAGE_PREFIX', '')

KALA_STORAGE_REGION = get_env_variable('KALA_STORAGE_REGION', 'us-west-1')

KALA_STORAGE_AUTHENTICATION_TYPE = get_env_variable('KALA_STORAGE_AUTHENTICATION_TYPE', 'credentials')
KALA_STORAGE_ACCESS_KEY = get_env_variable('KALA_ACCESS_KEY', 'minioadmin')
KALA_STORAGE_SECRET_KEY = get_env_variable('KALA_SECRET_KEY', 'minioadmin')

