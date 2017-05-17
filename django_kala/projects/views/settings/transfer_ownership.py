from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from accounts.mixins import AdminRequiredMixin
from projects.models import Project
from projects.forms import TransferOwnershipForm


class TransferOwnershipView(AdminRequiredMixin, TemplateView):
    template_name = 'settings/project_transfer_ownership.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        self.form = TransferOwnershipForm(request.POST or None, project=self.project)
        return super(TransferOwnershipView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('projects:transfer_ownership', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
