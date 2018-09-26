from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView


class PasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings/password.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'user': self.user,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(get_user_model().objects.all(), pk=pk)

        if not request.user.is_superuser and request.user != self.user:
            raise PermissionDenied(_('You do not have permission to edit this user.'))

        if request.user.is_superuser:
            self.form = SetPasswordForm(self.user, request.POST or None)
        else:
            self.form = PasswordChangeForm(self.user, request.POST or None)
        return super(PasswordView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('The password has been updated.'))
            return redirect(reverse('users:password', args=[self.user.pk]))
        return self.render_to_response(self.get_context_data())
