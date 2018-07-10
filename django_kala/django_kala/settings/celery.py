from .functions import get_env_variable

EXPORT_QUEUE = get_env_variable('EXPORT_QUEUE', default='exports')

CELERY_BROKER_URL = 'sqs://'
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': get_env_variable('AWS_REGION', default='us-west-2')}
CELERY_TASK_ROUTES = {
    'projects.tasks.export_project.ExportProjectTask': EXPORT_QUEUE,
    'projects.tasks.export_document.ExportDocumentTask': EXPORT_QUEUE,
}
