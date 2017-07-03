from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView

from companies.models import Company
from companies.forms import DetailsForm


class DetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/settings/details.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'organization': self.organization,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(Company.objects.active(), pk=pk)
        self.form = DetailsForm(request.POST or None, instance=self.organization)
        return super(DetailsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save(commit=False)
            self.form.save_m2m()
            self.form.save()
            return redirect(reverse('organizations:details', args=[self.organization.pk]))
        return self.render_to_response(self.get_context_data())
