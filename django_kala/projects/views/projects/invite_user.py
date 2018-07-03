from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from auth.models import Permissions
from projects.models import Project
from ...forms.invite_user import InviteUserForm


class InviteUserView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/invite_user.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form,
            'project': self.project,
            'organization': self.project.organization,
            'can_change': self.project.has_change(self.request.user),
            'can_create': self.project.has_change(self.request.user) or self.project.has_create(self.request.user),
            'can_invite': self.project.organization.has_change(
                self.request.user) or self.project.organization.has_create(self.request.user)
        }

    def dispatch(self, request, pk, *args, **kwargs):
        self.project = get_object_or_404(Project.objects.active(), pk=pk)
        if not Permissions.has_perms(
                [
                    'change_project',
                    'add_project',
                    'delete_project'
                ], request.user, self.project.uuid) and not Permissions.has_perms([
            'change_organization',
            'add_organization',
            'delete_organization'
        ], request.user, self.project.organization.uuid) and not self.project.document_set.filter(
            uuid__in=Permissions.objects.filter(
                permission__codename__in=[
                    'change_document',
                    'add_document',
                    'delete_document'
                ], user=request.user).values_list('object_uuid', flat=True)).exists():
            raise PermissionDenied(
                _('You do not have permission to view this project.')
            )

        # Do we have permission to add people?
        admin_permission = True if Permissions.has_perms(
            ['change_project'],
            request.user,
            self.project.uuid
        ) or Permissions.has_perms(
            ['change_organization'],
            request.user,
            self.project.organization.uuid
        ) else False
        self.form = InviteUserForm(request.POST or None, admin_permission=admin_permission)
        return super(InviteUserView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = user.email
            user.save()
            self.project.add_create(user)
            if self.form.cleaned_data['user_type'] == 'Admin':
                self.project.add_change(user)
                self.project.add_delete(user)

            user.send_invite(settings.EMAIL_APP, 'email/invite_project', _('Invitation to collaborate'), user)
            messages.success(request, _('The invitation has been sent.'))
            return redirect(reverse('projects:project_invite_user', args=[self.project.pk]))
        return self.render_to_response(self.get_context_data())
