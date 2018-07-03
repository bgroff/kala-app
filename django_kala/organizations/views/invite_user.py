from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from organizations.models import Organization
from projects.forms.invite_user import InviteUserForm


class InviteUserView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'organization': self.organization,
            'can_invite': self.can_invite,

        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(Organization.objects.active(), pk=pk)

        self.can_invite = self.organization.has_change(self.request.user) or self.organization.has_create(self.request.user)
        if not self.can_invite:
            raise PermissionDenied(_('You do not have permission to invite users to this organization.'))

        self.has_create = self.organization.has_create(request.user)
        self.has_change = self.organization.has_change(request.user)
        self.form = InviteUserForm(
            request.POST or None,
            admin_permission=(
                self.has_change and
                self.has_create and
                self.organization.has_delete(request.user)
            )
        )

        return super(InviteUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = user.email
            user.save()
            self.organization.add_create(user)
            if self.form.cleaned_data['user_type'] == 'Admin':
                self.organization.add_change(user)
                self.organization.add_delete(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_organization', _('Invitation to collaborate'), self.organization)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(
                reverse(
                    'organizations:invite_user',
                    args=[self.organization.pk]
                )
            )
        return self.render_to_response(self.get_context_data())
