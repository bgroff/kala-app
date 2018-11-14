# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404, redirect
# from django.urls import reverse
# from django.utils.decorators import method_decorator
# from django.utils.translation import ugettext as _
# from django.views.generic.base import TemplateView
#
# from projects.models import Project
#
#
# class ArchiveView(TemplateView):
#     template_name = 'projects/settings/archive.html'
#
#     def get_context_data(self, **kwargs):
#         return {
#             'project': self.project,
#             'organization': self.project.organization
#         }
#
#     @method_decorator(login_required)
#     def dispatch(self, request, pk, *args, **kwargs):
#         self.project = get_object_or_404(Project.objects.active(), pk=pk)
#         if not self.project.can_manage(request.user):
#             raise PermissionDenied(_('You do not have permission to archive this project'))
#
#         return super(ArchiveView, self).dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.project.set_active(False)
#         return redirect(reverse('projects:projects'))
