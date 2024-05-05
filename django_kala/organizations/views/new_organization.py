from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from ..forms.settings.details import DetailsForm


class NewOrganizationView(TemplateView):
    template_name = 'organizations/new_organization.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
        }

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied(_('You do not have permission to create a new organization.'))
        self.form = DetailsForm(request.POST or None, request.FILES or None)
        return super(NewOrganizationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            company = self.form.save()
            messages.success(request, _('The organization has been saved.'))
            return redirect(reverse('organizations:organization', args=[company.pk]))
        return self.render_to_response(self.get_context_data())
