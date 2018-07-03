from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.views.generic import TemplateView

from ..forms.invite_user import InviteUserForm


class InviteUserView(LoginRequiredMixin, TemplateView):
    template_name = 'invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form
        }

    def dispatch(self, request, *args, **kwargs):
        self.form = InviteUserForm(request.POST or None)
        return super(InviteUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = user.email
            user.save()
            for organization in self.form.cleaned_data['organizations']:
                organization.add_create(user)
                if self.form.cleaned_data['user_type'] == 'Admin':
                    organization.add_change(user)
                    organization.add_delete(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_user', _('Invitation to collaborate'), user)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(reverse('users:details', args=[user.pk]))
        return self.render_to_response(self.get_context_data())
