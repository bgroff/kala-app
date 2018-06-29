from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from projects.models import Project
from projects.forms import TransferOwnershipForm


class TransferOwnershipView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/transfer_ownership.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
            'organization': self.project.organization,
            'can_create': self.project.has_change(self.request.user) or self.project.has_create(self.request.user),
            'can_invite': self.project.organization.has_change(self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.has_change(request.user):
            raise PermissionDenied('You do not have permission to edit this project')

        self.form = TransferOwnershipForm(request.POST or None, project=self.project)
        return super(TransferOwnershipView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'The project has been transferred.')
            return redirect(reverse('projects:transfer_ownership', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
