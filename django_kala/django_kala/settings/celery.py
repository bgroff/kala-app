from .functions import get_env_variable

CELERY_BROKER_URL = 'sqs://'
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': get_env_variable('AWS_REGION', default='us-west-2')}
