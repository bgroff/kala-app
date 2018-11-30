from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView

from organizations.models import Organization
from organizations.tasks.delete_organization import DeleteOrganizationTask


class DeleteView(TemplateView):
    template_name = 'organizations/settings/delete.html'

    def get_context_data(self, **kwargs):
        return {
            'organization': self.organization
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(
            Organization.objects.active(),
            pk=pk
        )
        if not self.organization.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to delete this organization'))

        return super(DeleteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.organization.set_active(False)
        DeleteOrganizationTask().apply_async([self.organization.pk, request.user.pk], queue=settings.DELETE_QUEUE)
        messages.success(request, _('The organization has been delete.'))
        return redirect(
            reverse(
                'organizations:organizations',
            )
        )
