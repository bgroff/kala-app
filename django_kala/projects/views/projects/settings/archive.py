from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from accounts.mixins import AdminRequiredMixin
from projects.models import Project


class ArchiveView(AdminRequiredMixin, TemplateView):
    template_name = 'projects/settings/archive.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        return super(ArchiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.project.set_active(False)
        return redirect(reverse('projects:projects'))
