from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from auth.forms import DetailsForm


class DetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'user': self.user,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(get_user_model().objects.all(), pk=pk)

        if not request.user.is_superuser and request.user != self.user:
            raise PermissionDenied(_('You do not have permission to edit this user.'))

        self.form = DetailsForm(request.POST or None, instance=self.user)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, _('The user has been updated.'))
            return redirect(reverse('users:details', args=[self.user.pk]))
        return self.render_to_response(self.get_context_data())
