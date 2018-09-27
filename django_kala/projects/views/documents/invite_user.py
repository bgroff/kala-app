from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from documents.models import Document
from projects.models import Project
from ...forms.invite_user import InviteUserForm, EmailForm

User = get_user_model()


class InviteUserView(LoginRequiredMixin, TemplateView):
    template_name = 'documents/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'email_form': self.email_form,
            'project': self.project,
            'organization': self.project.organization,
            'document': self.document,
            'can_manage': self.document.can_manage(self.request.user),
            'can_create': self.document.can_create(self.request.user),
            'can_invite': self.document.can_invite(self.request.user)
        }

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=project_pk)
        self.document = get_object_or_404(
            Document.objects.active().prefetch_related(
                'documentversion_set',
                'documentversion_set__user'
            ),
            pk=document_pk)

        if not self.document.can_invite(self.request.user):
            raise PermissionDenied(_('You do not have permissions to invite users to this document.'))

        self.email_form = EmailForm(request.POST or None)
        self.form = InviteUserForm(
            request.POST or None,
            manager=self.document.can_manage(self.request.user)
        )

        return super(InviteUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.email_form.is_valid() and self.form.is_valid():
            try:
                user = User.objects.get(email=self.email_form.cleaned_data['email'])
            except User.DoesNotExist:
                user = self.form.save(commit=False)
                user.email = self.email_form.cleaned_data['email']
                user.username = user.email
                user.save()
            if self.form.cleaned_data['user_type'] == 'manager':
                self.document.add_delete(user)
            elif self.form.cleaned_data['user_type'] == 'collaborator':
                self.project.add_invite(user)
            else:
                self.document.add_create(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_document', _('Invitation to collaborate'), user)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(
                reverse(
                    'projects:document_invite_user',
                    args=[self.project.pk, self.document.pk]
                )
            )
        return self.render_to_response(self.get_context_data())
