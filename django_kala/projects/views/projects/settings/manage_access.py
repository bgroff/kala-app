from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from projects.forms import manage_access_forms
from projects.models import Project


class ManageAccessView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/settings/manage_access.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'project': self.project,
            'organization': self.project.organization,
            'can_create': self.project.has_change(self.request.user) or self.project.has_create(self.request.user),
            'can_invite': self.project.organization.has_change(self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.has_change(request.user):
            raise PermissionDenied('You do not have permission to edit this project')

        self.forms = manage_access_forms(request, self.project)
        return super(ManageAccessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_valid = True
        for form in self.forms:
            if form.is_valid():
                form.save()
            else:
                all_valid = False
        if all_valid:
            messages.success(request, 'The permissions have been updated.')
            return redirect(reverse('projects:manage_access', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
