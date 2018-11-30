from django_kala.functions import get_env_variable

EXPORT_QUEUE = get_env_variable('EXPORT_QUEUE', default='exports')
DELETE_QUEUE = get_env_variable('DELETE_QUEUE', default='deletes')

CELERY_BROKER_URL = 'sqs://'
CELERY_BROKER_TRANSPORT_OPTIONS = {'region': get_env_variable('AWS_REGION', default='us-west-2')}
CELERY_TASK_ROUTES = {
    'organizations.tasks.delete_organization.DeleteOrganizationTask': DELETE_QUEUE,
    'projects.tasks.delete_document.DeleteDocumentTask': DELETE_QUEUE,
    'projects.tasks.delete_project.DeleteProjectTask': DELETE_QUEUE,

    'projects.tasks.export_project.ExportProjectTask': EXPORT_QUEUE,
    'projects.tasks.export_document.ExportDocumentTask': EXPORT_QUEUE,
}
