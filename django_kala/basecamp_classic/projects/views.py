from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from projects.models import Project

from .parsers import XMLProjectParser
from .renderers import XMLProjectRenderer
from .serializers import ProjectSerializer

from ..people.parsers import XMLParser
from ..people.renderers import XMLPeopleRenderer


class ProjectsView(APIView):
    """
    View that will display XML for all projects.

    """
    parser_classes = [XMLProjectParser]
    renderer_classes = [XMLProjectRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication

    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return an xml version of all of the companies.
        """
        return Response({'projects': Project.objects.all().prefetch_related(), 'request_user': request.user})

    def post(self, request, format=None):
        if not request.user.is_admin:
            raise PermissionDenied()

        project_data = ProjectSerializer(data=request.data)
        if project_data.is_valid():
            project = project_data.save()
            return Response({'projects': project, 'request_user': request.user}, status=HTTP_201_CREATED)
        return Response(project_data.errors, status=HTTP_400_BAD_REQUEST)


class ProjectView(APIView):
    """
    View a single project by pk.
    """
    parser_classes = [XMLProjectParser]
    renderer_classes = [XMLProjectRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return a company by pk.
        """
        project = get_object_or_404(Project, pk=pk)
        return Response({'projects': project, 'request_user': request.user})


class PeopleView(APIView):
    """
    View to show a all users associated with a project.
    """
    parser_classes = [XMLParser]
    renderer_classes = [XMLPeopleRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return a list of all users for a specific project.
        """
        project = get_object_or_404(Project, pk=pk)
        return Response({'users': project.clients.all(), 'request_user': request.user})
