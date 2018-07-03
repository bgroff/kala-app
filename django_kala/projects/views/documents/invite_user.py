from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from documents.models import Document
from projects.models import Project
from ...forms.invite_user import InviteUserForm


class InviteUserView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
            'organization': self.project.organization,
            'document': self.document,
            'can_change': self.document.has_change(self.request.user),
            'can_create': self.has_change or self.has_create,
            'can_invite': self.project.organization.has_change(
                self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(
            Document.objects.active().prefetch_related(
                'documentversion_set',
                'documentversion_set__user'
            ),
            pk=document_pk)
        self.has_create = self.document.has_create(request.user)
        self.has_change = self.document.has_change(request.user)
        if not self.has_create and not self.has_change and not self.document.has_delete(request.user):
            raise PermissionDenied(_('You do not have permissions to view this document.'))
        self.form = InviteUserForm(
            request.POST or None,
            admin_permission=(
                self.has_change and
                self.has_create and
                self.document.has_delete(request.user)
            )
        )

        return super(InviteUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = user.email
            user.save()
            self.document.add_create(user)
            if self.form.cleaned_data['user_type'] == 'Admin':
                self.document.add_change(user)
                self.document.add_delete(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_document', _('Invitation to collaborate'), user)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(
                reverse(
                    'projects:document_invite_user',
                    args=[self.project.pk, self.document.pk]
                )
            )
        return self.render_to_response(self.get_context_data())
