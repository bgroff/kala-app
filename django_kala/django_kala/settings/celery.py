from .functions import get_env_variable

# Celery Configuration
DEPLOYMENT_ENVIRONMENT = get_env_variable('DEPLOYMENT_ENVIRONMENT')
if DEPLOYMENT_ENVIRONMENT == 'production':
    # If we are in production, use SQS
    AWS_REGION = get_env_variable('AWS_REGION', default='us-west-2')
    CELERY_BROKER_URL = 'sqs://@'
    CELERY_BROKER_TRANSPORT_OPTIONS = {'region': AWS_REGION}
    CELERY_SEND_TASK_ERROR_EMAILS = True

# The global default rate limit for tasks.  The default is no rate limit.
# http://docs.celeryproject.org/en/latest/configuration.html#celery-default-rate-limit
CELERY_DEFAULT_RATE_LIMIT = '1/s'

CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'

# How many messages to prefetch at a time; default is 4
# http://docs.celeryproject.org/en/latest/configuration.html#celeryd-prefetch-multiplier
CELERYD_PREFETCH_MULTIPLIER = 1

# Task messages will be retried in the case of connection loss or other
# connection errors
# http://docs.celeryproject.org/en/latest/configuration.html#celery-task-publish-retry
CELERY_TASK_PUBLISH_RETRY = True

# Defines the default policy when retrying publishing a task message in the
# case of connection loss or other connection errors
# http://docs.celeryproject.org/en/latest/configuration.html#celery-task-publish-retry-policy
CELERY_TASK_PUBLISH_RETRY_POLICY = {
    'max_retries': 3,
}

# Disabling rate limits altogether is recommended if you don't have any tasks
# using them.
# http://docs.celeryproject.org/en/latest/userguide/tasks.html#disable-rate-limits-if-they-re-not-used
CELERY_DISABLE_RATE_LIMITS = True

# Late ack means the task messages will be acknowledged after the task has been
# executed, not just before, which is the default behavior.
# http://docs.celeryproject.org/en/latest/configuration.html#celery-acks-late
CELERY_ACKS_LATE = True
