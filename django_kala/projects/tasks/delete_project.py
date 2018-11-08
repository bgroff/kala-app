from celery.task import Task
from django.contrib.auth import get_user_model

from projects.models import Project
from projects.tasks.delete_document import DeleteDocumentTask

User = get_user_model()


class DeleteProjectTask(Task):

    def run(self, *args, **kwargs):
        self.project = Project.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        if not self.project.can_manage(user):
            # TODO: Log this
            return
        for document in self.project.document_set.all():
            DeleteDocumentTask().apply_async([document.pk, user.pk])

    def on_success(self, retval, task_id, args, kwargs):
        self.project.delete()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Log this
        return
