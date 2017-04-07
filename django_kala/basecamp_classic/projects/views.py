from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from projects.models import Project, Category

from .parsers import XMLProjectParser, XMLCategoryParser
from .renderers import XMLProjectRenderer, XMLCategoryRenderer
from .serializers import ProjectSerializer, CategorySerializer
from ..documents.parsers import XMLDocumentParser
from ..documents.renderers import XMLDocumentRenderer
from ..documents.serializers import DocumentSerializer

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


class CategoriesView(APIView):
    """
    View that will display XML for all categories for a project.

    """
    parser_classes = [XMLCategoryParser]
    renderer_classes = [XMLCategoryRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return an xml version of all of the companies.
        """
        project = get_object_or_404(Project, pk=pk)
        return Response({'categories': project.category_set.all().prefetch_related(), 'request_user': request.user})

    def post(self, request, pk, format=None):
        if not request.user.is_admin:
            raise PermissionDenied()

        project = get_object_or_404(Project, pk=pk)
        category_data = CategorySerializer(data=request.data, project=project)
        if category_data.is_valid():
            category = category_data.save()
            return Response({'categories': category, 'request_user': request.user}, status=HTTP_201_CREATED)
        return Response(category_data.errors, status=HTTP_400_BAD_REQUEST)


class DocumentsView(APIView):
    """
    View that will display XML for all categories for a project.

    """
    parser_classes = [XMLDocumentParser]
    renderer_classes = [XMLDocumentRenderer]
    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication
    )
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        """
        Return an xml version of all of the companies.
        """
        project = get_object_or_404(Project, pk=pk)
        return Response({'documents': project.document_set.all().prefetch_related(), 'request_user': request.user})

    def post(self, request, pk, format=None):
        if not request.user.is_admin:
            raise PermissionDenied()

        project = get_object_or_404(Project, pk=pk)
        document_data = DocumentSerializer(data=request.data, project=project)
        if document_data.is_valid():
            document = document_data.save()
            return Response({'documents': document, 'request_user': request.user}, status=HTTP_201_CREATED)
        return Response(document_data.errors, status=HTTP_400_BAD_REQUEST)
