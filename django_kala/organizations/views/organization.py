from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import TemplateView

from organizations.models import Organization


class OrganizationView(TemplateView):
    template_name = 'organizations/organization.html'

    def get_context_data(self, **kwargs):
        per_page = self.request.GET.get('per_page', 20)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(self.projects, per_page)
        try:
            projects = paginator.page(page).object_list
        except InvalidPage:
            projects = paginator.page(1)
        return {
            'organization': self.organization,
            'projects': projects,
            'page_range': paginator.page_range,
            'current_page': page,
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.organization = get_object_or_404(Organization.objects.active().prefetch_related('project_set'), pk=pk)
        self.projects = self.organization.get_projects(user=self.request.user)
        if not self.organization.can_create(user=self.request.user):
            raise PermissionDenied(
                _('You do not have permission to view this organization.')
            )

        return super(OrganizationView, self).dispatch(request, *args, **kwargs)
