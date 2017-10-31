from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from projects.models import Project
from projects.forms.settings import manage_access_forms


class ArchiveView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/archive.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'users': self.project.get_users(self.request.user),
            'forms': self.forms,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.has_change(request.user) \
                or not self.project.has_delete(request.user) \
                or not self.project.has_add(request.user):
            raise PermissionDenied('You do not have permission to edit this project')
        self.forms = manage_access_forms(request, self.project)
        return super(ArchiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return redirect(reverse('projects:projects'))
