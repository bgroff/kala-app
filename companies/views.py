from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from ndptc.accounts.mixins import AdminRequiredMixin
from .forms import CompanyForm, DeletedPeopleForm
from .models import Company


class CompanyView(AdminRequiredMixin, TemplateView):
    template_name = 'company.html'

    def get_context_data(self, **kwargs):
        return {
            'company': self.company,
            'form': self.form,
            'undelete_form': self.undelete_form,
            }

    def dispatch(self, request, pk, *args, **kwargs):
        self.company = get_object_or_404(Company.objects.active(), pk=pk)
        self.form = CompanyForm(request.POST or None, instance=self.company)
        self.undelete_form = DeletedPeopleForm(request.POST or None, company=self.company)
        return super(CompanyView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            self.company.set_active(False)
            messages.success(request, 'The company %s has been deleted' % self.company)
            return redirect(reverse('accounts'))

        if 'undelete' in request.POST and self.undelete_form.is_valid():
            person = self.undelete_form.save()
            messages.success(request, 'The person %s has been un-deleted' % person)
            return redirect(reverse('company', args=[self.company.pk]))

        if 'update' in request.POST and self.form.is_valid():
            self.form.save()
            messages.success(request, 'The company information has been updated')
            return redirect(reverse('company', args=[self.company.pk]))

        return self.render_to_response(self.get_context_data())
