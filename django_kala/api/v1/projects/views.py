from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# from api.v1.serializers.permission_serializer import PermissionsSerializer
from projects.models import Project


class ProjectsView(APIView):
    pass


class ProjectView(APIView):
    pass


class DocumentsView(APIView):
    pass


class DocumentView(APIView):
    pass

#
# class ProjectPermissionsView(ListCreateAPIView, UpdateModelMixin):
#     serializer_class = PermissionsSerializer
#     queryset = Permissions.objects.all().select_related('permission').prefetch_related('permission')
#
#     def dispatch(self, request, pk, *args, **kwargs):
#         self.project = get_object_or_404(Project.objects.active(), pk=pk)
#         if not Permissions.has_perms(
#                 [
#                     'change_project',
#                     'add_project',
#                     'delete_project'
#                 ], request.user, self.project.uuid) and not Permissions.has_perms([
#                     'change_organization',
#                     'add_organization',
#                     'delete_organization'
#                 ], request.user, self.project.organization.uuid) and not self.project.document_set.filter(
#             uuid__in=Permissions.objects.filter(
#                 permission__codename__in=[
#                     'change_document',
#                     'add_document',
#                     'delete_document'
#                 ], user=request.user).values_list('object_uuid', flat=True)).exists():
#             raise PermissionDenied(
#                 _('You do not have permission to view this project.')
#             )
#         return super(ProjectPermissionsView, self).dispatch(request, *args, **kwargs)
#
#     def list(self, request, *args, **kwargs):
#         permissions = self.queryset.filter(object_uuid=self.project.uuid)
#         serializer = self.serializer_class(permissions, many=True)
#         return Response(serializer.data)
