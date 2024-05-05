from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateView

from projects.models import Project
from projects.tasks.delete_project import DeleteProjectTask


class DeleteView(TemplateView):
    template_name = 'projects/settings/delete.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(
            Project.objects.active().select_related(
                'organization'
            ),
            pk=pk
        )
        if not self.project.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to delete this project'))

        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.project.set_active(False)
        DeleteProjectTask().apply_async([self.project.pk, request.user.pk], queue=settings.DELETE_QUEUE)
        messages.success(request, _('The project has been delete.'))
        return redirect(
            reverse(
                'organizations:organization',
                args=[
                    self.project.organization.pk,
                ]
            )
        )
