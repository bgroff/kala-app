from api.v1.projects.settings.serializers import DocumentPermissionSerializer
from django.contrib.auth import get_user_model
from django.db import connections
from django.shortcuts import get_object_or_404
from documents.models import Document, DocumentPermission
from projects.models import Project
from psycopg2.extras import NamedTupleCursor
from rest_framework.exceptions import PermissionDenied, NotFound, APIException
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


User = get_user_model()


class ProjectsView(APIView):
    pass


class ProjectView(APIView):
    pass


class DocumentsView(APIView):
    pass


class DocumentView(APIView):
    pass


class DocumentPermissionsView(CreateAPIView, ListAPIView):
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

    def get_serializer_context(self):
        context = super(DocumentPermissionsView, self).get_serializer_context()
        context.update({
            'user': self.request.user,
            'document': self.document
        })
        return context

    def get_queryset(self):
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
                           (select codename from auth_permission where id = documents_documentpermission.permission_id) as permission,
                           (select codename from auth_permission where id = projects_projectpermission.permission_id) as project_permission,
                           (select codename from auth_permission where id = organizations_organizationpermission.permission_id) as organization_permission
                    FROM   kala_user
                           LEFT JOIN documents_documentpermission
                                  ON documents_documentpermission.user_id = kala_user.id
                           LEFT JOIN kala_documents
                                  ON kala_documents.id = %s
                           LEFT JOIN kala_projects
                                  ON kala_projects.id = %s
                           LEFT JOIN kala_companies
                                  ON kala_companies.id = %s
                           LEFT JOIN projects_projectpermission
                                  ON projects_projectpermission.project_id = kala_projects.id
                                     AND projects_projectpermission.user_id = kala_user.id
                           LEFT JOIN organizations_organizationpermission
                                  ON organizations_organizationpermission.organization_id = kala_projects.organization_id
                                     AND organizations_organizationpermission.user_id = kala_user.id
                    WHERE document_id = %s OR kala_user.id in %s ORDER BY last_name;
                    """, [self.document.id, self.document.project.id, self.document.project.organization.id, self.document.id, tuple(self.available_users)])
            return cursor.fetchall()


class DocumentPermissionView(UpdateAPIView, DestroyAPIView):
    serializer_class = DocumentPermissionSerializer
    permission_classes = []
    queryset = DocumentPermission.objects.all()

    def dispatch(self, request, project_pk, document_pk, pk, *args, **kwargs):
        try:
            self.project = get_object_or_404(Project.objects.select_related(), pk=project_pk)
            self.document = get_object_or_404(Document, pk=document_pk)
            self.permission = get_object_or_404(DocumentPermission, pk=pk)

            if not self.document.can_manage(request.user):
                raise PermissionDenied('You do not have permission to modify this documents permission')

            if self.document.project.id != self.project.id:
                raise NotFound('The document does not exist')

            if self.permission.document.pk != self.document.pk:
                raise NotFound('The permission does not exist')

            kwargs['pk'] = pk
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            raise APIException(str(e))

    def get_serializer_context(self):
        context = super(DocumentPermissionView, self).get_serializer_context()
        context.update({
            'user': self.request.user,
            'document': self.document
        })
        return context
