from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from projects.forms.documents.settings.manage_access import manage_access_forms
from documents.models import Document


class ManageAccessView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/settings/manage_access.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'document': self.document,
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.document = get_object_or_404(
            Document.objects.active().select_related(
                'project',
                'project__organization'
            ),
            pk=document_pk
        )
        if not self.document.has_change(request.user):
            raise PermissionDenied('You do not have permission to edit this project')

        self.forms = manage_access_forms(request, self.document)
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
            return redirect(
                reverse(
                    'projects:document_manage_access',
                    args=[
                        self.document.project.pk,
                        self.document.pk
                    ]
                )
            )
        return self.render_to_response(self.get_context_data())
