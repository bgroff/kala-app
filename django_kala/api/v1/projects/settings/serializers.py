from rest_framework import serializers
from documents.models import DocumentPermission


class DocumentPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    document_id = serializers.IntegerField(required=True)
    document_name = serializers.IntegerField(required=False)
    project_id = serializers.IntegerField(required=False)
    project_name = serializers.IntegerField(required=False)
    organization_id = serializers.IntegerField(required=False)
    organization_name = serializers.IntegerField(required=False)
    document_permission = serializers.ChoiceField(required=True,
                                                  choices=[('can_invite', 'Can invite'), ('can_create', 'Can create'),
                                                           ('can_manage', 'Can manage')])
    project_permission = serializers.ChoiceField(required=False,
                                                 choices=[('can_invite', 'Can invite'), ('can_create', 'Can create'),
                                                          ('can_manage', 'Can manage')])
    organization_permission = serializers.ChoiceField(required=False, choices=[('can_invite', 'Can invite'),
                                                                               ('can_create', 'Can create'),
                                                                               ('can_manage', 'Can manage')])

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'user': {
                'id': obj.user_id,
                'username': obj.username,
                'first_name': obj.first_name,
                'last_name': obj.last_name
            },
            'document': {
                'id': obj.document_id,
                'name': obj.document_name,
                'permission': obj.document_permission
            },
            'project': {
                'id': obj.project_id,
                'name': obj.project_name,
                'permission': obj.project_permission
            },
            'organization': {
                'id': obj.organization_id,
                'name': obj.organization_name,
                'permission': obj.organization_permission
            }
        }
