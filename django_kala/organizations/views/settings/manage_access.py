from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from auth.forms.manage_access import manage_access_forms
from django_kala.functions import create_user_permissions
from organizations.models import Organization, OrganizationPermission

import json


class ManageAccessView(TemplateView):
    template_name = 'organizations/settings/manage_access.html'

    def get_context_data(self, **kwargs):
        permissions = OrganizationPermission.objects.filter(**{
            'organization': self.organization,
            'user__in': self.request.user.get_users()
        }).select_related(
            'permission',
            'user'
        )

        users = create_user_permissions(permissions, self.request.user.get_users())

        return {
            'forms': self.forms,
            'organization': self.organization,
            'users': json.dumps(users),
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(
            Organization.objects.active(),
            pk=pk
        )
        if not self.organization.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to edit this project'))

        self.forms = manage_access_forms(request, self.organization, OrganizationPermission, field='organization')
        return super(ManageAccessView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        all_valid = True
        for form in self.forms:
            if form.is_valid():
                form.save()
            else:
                all_valid = False
        if all_valid:
            messages.success(request, _('The permissions have been updated.'))
            return redirect(
                reverse(
                    'organizations:manage_access',
                    args=[
                        self.organization.pk
                    ]
                )
            )
        return self.render_to_response(self.get_context_data())
