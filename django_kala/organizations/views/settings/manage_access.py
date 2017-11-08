from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from organizations.forms.settings.manage_access import manage_access_forms
from organizations.models import Organization


class ManageAccessView(LoginRequiredMixin, TemplateView):
    template_name = 'organizations/settings/manage_access.html'

    def get_context_data(self, **kwargs):
        return {
            'forms': self.forms,
            'organization': self.organization,
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(
            Organization.objects.active(),
            pk=pk
        )
        if not self.organization.has_change(request.user):
            raise PermissionDenied('You do not have permission to edit this project')

        self.forms = manage_access_forms(request, self.organization)
        return super(ManageAccessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_valid = True
        for form in self.forms:
            if form.is_valid():
                form.save()
            else:
                all_valid = False
        if all_valid:
            messages.success(request, 'The permissions have been updated.')
            return redirect(
                reverse(
                    'organizations:manage_access',
                    args=[
                        self.organization.pk
                    ]
                )
            )
        return self.render_to_response(self.get_context_data())
