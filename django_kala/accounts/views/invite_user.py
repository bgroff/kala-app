from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import TemplateView

from ..forms.invite_user import InviteUserForm
from ..mixins import LoginRequiredMixin


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
            user.send_invite()
            return redirect(reverse('users:details', args=[user.pk]))
        return self.render_to_response(self.get_context_data())
