from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from projects.models import Project
from ...forms.invite_user import InviteUserForm, EmailForm

User = get_user_model()


class InviteUserView(TemplateView):
    template_name = 'projects/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'email_form': self.email_form,
            'project': self.project,
            'organization': self.project.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.can_invite(self.request.user):
            raise PermissionDenied(
                _('You do not have permission to view this project.')
            )

        self.form = InviteUserForm(request.POST or None, manager=self.project.can_manage(self.request.user))
        self.email_form = EmailForm(request.POST or None)
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
                self.project.add_manage(user)
            elif self.form.cleaned_data['user_type'] == 'collaborator':
                self.project.add_invite(user)
            else:
                self.project.add_create(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_project', _('Invitation to collaborate'), user)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(reverse('projects:project_invite_user', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
