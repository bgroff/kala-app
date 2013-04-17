from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from kala.views import AdminRequiredMixin
from .forms import CompanyForm
from .models import Companies


class CompanyView(AdminRequiredMixin, TemplateView):
    template_name = 'company.html'

    def get_context_data(self, **kwargs):
        return {
            'company': self.company,
            'form': self.form,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.company = get_object_or_404(Companies.active, pk=pk)
        self.form = CompanyForm(request.POST or None, instance=self.company)
        return super(CompanyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            self.company.set_active(False)
            return redirect(reverse('people'))

        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'The company information has been updated')
            return redirect(reverse('company', args=[self.company.pk]))

        return self.render_to_response(self.get_context_data())
