from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from projects.forms import manage_access_forms
from projects.models import Project, ProjectPermission


class ManageAccessView(TemplateView):
    template_name = 'projects/settings/manage_access.html'

    def get_context_data(self, **kwargs):
        permissions = ProjectPermission.objects.filter(**{
            'project': self.project,
            "user__in": self.request.user.get_users()
        }).select_related(
            'permission',
            'user'
        )

        users = [{
            'user': user,
            'can_create': True if 'can_create' in permissions.filter(user=user).values_list(
                'permission__codename', flat=True) else False,
            'can_invite': True if 'can_invite' in permissions.filter(user=user).values_list(
                'permission__codename', flat=True) else False,
            'can_manage': True if 'can_manage' in permissions.filter(user=user).values_list(
                'permission__codename', flat=True) else False,
        } for user in self.request.user.get_users()]

        return {
            'forms': self.forms,
            'project': self.project,
            'organization': self.project.organization,
            'users': users
        }

    @method_decorator(login_required)
    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not self.project.can_manage(request.user):
            raise PermissionDenied(_('You do not have permission to edit this project'))

        self.forms = manage_access_forms(request, self.project, ProjectPermission, field='project')
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
            return redirect(reverse('projects:manage_access', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
