from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from organizations.models import Organization
from projects.forms.invite_user import InviteUserForm, EmailForm

User = get_user_model()


class InviteUserView(TemplateView):
    template_name = 'organizations/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'email_form': self.email_form,
            'organization': self.organization,
            'can_invite': self.can_invite,
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(Organization.objects.active(), pk=pk)

        self.can_invite = self.organization.can_invite(self.request.user)
        if not self.can_invite:
            raise PermissionDenied(_('You do not have permission to invite users to this organization.'))

        self.email_form = EmailForm(request.POST or None)
        self.form = InviteUserForm(
            request.POST or None,
            manager=self.organization.can_manage(self.request.user)
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
                self.organization.add_manage(user)
            elif self.form.cleaned_data['user_type'] == 'collaborator':
                self.organization.add_invite(user)
            else:
                self.organization.add_create(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_organization', _('Invitation to collaborate'), self.organization)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(
                reverse(
                    'organizations:invite_user',
                    args=[self.organization.pk]
                )
            )
        return self.render_to_response(self.get_context_data())
