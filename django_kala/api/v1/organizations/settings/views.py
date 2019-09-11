from api.v1.organizations.settings.serializers import OrganizationPermissionSerializer, OrganizationPermissionSerializer
from django.contrib.auth import get_user_model
from django.db import connections
from django.shortcuts import get_object_or_404
from organizations.models import Organization, OrganizationPermission
from psycopg2.extras import NamedTupleCursor
from rest_framework.exceptions import PermissionDenied, NotFound, APIException
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

User = get_user_model()


class OrganizationPermissionsView(CreateAPIView, ListAPIView):
    serializer_class = OrganizationPermissionSerializer
    permission_classes = []

    def dispatch(self, request, organization_pk, *args, **kwargs):
        try:
            self.organization = get_object_or_404(Organization.objects.select_related(), pk=organization_pk)

            if not self.organization.can_manage(request.user):
                raise PermissionDenied('You do not have permission to modify this projects permission')

            self.available_users = request.user.get_users().values_list('id', flat=True)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            raise APIException(str(e))

    def get_serializer_context(self):
        context = super(OrganizationPermissionsView, self).get_serializer_context()
        context.update({
            'user': self.request.user,
            'organization': self.organization
        })
        return context

    def get_queryset(self):
        connection = connections['default']
        connection.ensure_connection()
        with connection.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute("""
                    SELECT organizations_organizationpermission.id,
                           kala_user.id as user_id,
                           username,
                           first_name,
                           last_name,
                           kala_companies.id AS organization_id,
                           kala_companies.name AS organization_name,
                           (select codename from auth_permission where id = organizations_organizationpermission.permission_id) as organization_permission
                    FROM   kala_user
                           LEFT JOIN organizations_organizationpermission
                                  ON organizations_organizationpermission.user_id = kala_user.id AND organizations_organizationpermission.id = %s
                           LEFT JOIN kala_companies
                                  ON kala_companies.id = %s
                    WHERE kala_user.id in %s ORDER BY last_name;
                    """, [self.organization.id, self.organization.id, tuple(self.available_users),])
            return cursor.fetchall()


class OrganizationPermissionView(UpdateAPIView, DestroyAPIView):
    serializer_class = OrganizationPermissionSerializer
    permission_classes = []
    queryset = OrganizationPermission.objects.all()

    def dispatch(self, request, organization_pk, pk, *args, **kwargs):
        try:
            self.organization = get_object_or_404(Organization.objects.select_related(), pk=organization_pk)
            self.permission = get_object_or_404(OrganizationPermission, pk=pk)

            if not self.organization.can_manage(request.user):
                raise PermissionDenied('You do not have permission to modify this organization permission')

            if self.permission.organization.pk != self.organization.pk:
                raise NotFound('The permission does not exist')

            kwargs['pk'] = pk
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            raise APIException(str(e))

    def get_serializer_context(self):
        context = super(OrganizationPermissionView, self).get_serializer_context()
        context.update({
            'user': self.request.user,
            'organization': self.organization
        })
        return context
