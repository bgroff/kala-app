from django.db import connections
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import PermissionDenied, NotFound, APIException
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

from psycopg2.extras import NamedTupleCursor


from api.v1.projects.settings.serializers import DocumentPermissionSerializer
from auth.models import User
from documents.models import Document
from projects.models import Project



class ProjectsView(APIView):
    pass


class ProjectView(APIView):
    pass


class DocumentsView(APIView):
    pass


class DocumentView(APIView):
    pass


class DocumentPermissionsView(CreateAPIView, ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentPermissionSerializer
    permission_classes = []

    def dispatch(self, request, project_pk, document_pk, *args, **kwargs):
        try:
            self.project = get_object_or_404(Project.objects.select_related(), pk=project_pk)
            self.document = get_object_or_404(Document, pk=document_pk)

            if not self.document.can_manage(request.user):
                raise PermissionDenied('You do not have permission to modify this documents permission')

            if self.document.project.id != self.project.id:
                raise NotFound('The document does not exist')

            self.available_users = request.user.get_users().values_list('id', flat=True)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            raise APIException(str(e))

    def list(self, request, *args, **kwargs):
        connection = connections['default']
        connection.ensure_connection()
        with connection.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("""
            SELECT documents_documentpermission.id,
                   kala_user.id as user_id,
                   username,
                   first_name,
                   last_name,
                   kala_documents.id AS document_id,
                   kala_documents.name AS document_name,
                   kala_projects.id  AS project_id,
                   kala_projects.name  AS project_name,
                   kala_companies.id AS organization_id,
                   kala_companies.name AS organization_name,
                   (select codename from auth_permission where id = documents_documentpermission.permission_id) as document_permission,
                   (select codename from auth_permission where id = projects_projectpermission.permission_id) as project_permission,
                   (select codename from auth_permission where id = organizations_organizationpermission.permission_id) as organization_permission
            FROM   kala_user
                   LEFT JOIN documents_documentpermission
                          ON documents_documentpermission.user_id = kala_user.id
                   LEFT JOIN kala_documents
                          ON kala_documents.id = document_id
                   LEFT JOIN kala_projects
                          ON kala_projects.id = kala_documents.project_id
                   LEFT JOIN kala_companies
                          ON kala_companies.id = kala_projects.organization_id
                   LEFT JOIN projects_projectpermission
                          ON projects_projectpermission.project_id = kala_projects.id
                             AND projects_projectpermission.user_id =
                                 documents_documentpermission.user_id
                   LEFT JOIN organizations_organizationpermission
                          ON organizations_organizationpermission.organization_id = kala_projects.organization_id
                             AND organizations_organizationpermission.user_id =
                                 documents_documentpermission.user_id
            WHERE document_id = %s OR kala_user.id in %s;
            """, [self.document.id, tuple(self.available_users)])
            s = DocumentPermissionSerializer(cursor.fetchall(), many=True)
            return Response(s.data)
