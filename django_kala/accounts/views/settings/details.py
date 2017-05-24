from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from accounts.mixins import AdminRequiredMixin
from accounts.forms import DetailsForm


class DetailsView(AdminRequiredMixin, TemplateView):
    template_name = 'accounts/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'user': self.user,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.user = get_object_or_404(get_user_model().objects.all(), pk=pk)
        self.form = DetailsForm(request.POST or None, instance=self.user)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('users:details', args=[self.user.pk]))
        return self.render_to_response(self.get_context_data())
