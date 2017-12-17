from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from projects.models import Project
from projects.forms.documents.new_document import NewDocumentForm, NewDocumentVersionForm


class NewDocumentView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/new_document.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'version_form': self.version_form,
            'project': self.project,
            'can_create': self.project.has_change(self.request.user) or self.project.has_create(self.request.user),
            'can_invite': self.project.organization.has_change(self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, project_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        if not self.project.has_create(request.user):
            raise PermissionDenied('You do not have permission to create a new document for this project.')
        self.form = NewDocumentForm(request.POST or None, project=self.project)
        self.version_form = NewDocumentVersionForm(
            request.POST or None,
            request.FILES or None,
            project=self.project,
            user=request.user
        )
        return super(NewDocumentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid() and self.version_form.is_valid():
            document = self.form.save(commit=False)
            document.save()
            version = self.version_form.save(document)
            document.name = request.FILES['file'].name
            document.save()
            version.name = request.FILES['file'].name
            version.mime = request.FILES['file'].content_type
            version.save()
            self.form.save_m2m()
            return redirect(reverse('projects:document', args=[self.project.pk, document.pk]))
        return self.render_to_response(self.get_context_data())
