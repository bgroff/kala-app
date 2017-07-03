from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..forms.settings.details import DetailsForm


class NewCompanyView(LoginRequiredMixin, TemplateView):
    template_name = 'companies/new_company.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
        }

    def dispatch(self, request, *args, **kwargs):
        self.form = DetailsForm(request.POST or None, request.FILES or None)
        return super(NewCompanyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            company = self.form.save()
            return redirect(reverse('organizations:organization', args=[company.pk]))
        return self.render_to_response(self.get_context_data())
