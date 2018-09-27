from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from projects.models import Project


class ArchiveView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/archive.html'

    def get_context_data(self, **kwargs):
        return {
            'project': self.project,
            'organization': self.project.organization,
            'can_create': self.project.can_create(self.request.user),
            'can_invite': self.project.can_invite(self.request.user)
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to archive this project'))

        return super(ArchiveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.project.set_active(False)
        return redirect(reverse('projects:projects'))
