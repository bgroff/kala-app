from celery.task import Task
from django.contrib.auth import get_user_model

from organizations.models import Organization
from projects.tasks.delete_project import DeleteProjectTask

User = get_user_model()


class DeleteOrganizationTask(Task):

    def run(self, *args, **kwargs):
        self.organization = Organization.objects.get(pk=args[0])
        user = User.objects.get(pk=args[1])
        if not self.organization.can_manage(user):
            # TODO: Log this
            return
        for project in self.organization.project_set.all():
            DeleteProjectTask().apply_async([project.pk, user.pk])

    def on_success(self, retval, task_id, args, kwargs):
        self.organization.delete()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: Log this
        return
