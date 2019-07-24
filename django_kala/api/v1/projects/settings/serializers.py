from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
        representation = {
            'id': obj.id,
            'user': {
                'id': obj.user_id,
                'username': obj.username,
                'first_name': obj.first_name,
                'last_name': obj.last_name
            }
        }
        if obj.document_permission:
            representation['document_permission'] = obj.document_permission

        if obj.project_permission:
            representation['project_permission'] = obj.project_permission
        if obj.organization_permission:
            representation['organization_permission'] = obj.organization_permission
        return representation

    def create(self, validated_data):
        user = self.context.get('user')
        document = self.context.get('document')
        if validated_data['document_permission'] == 'can_invite':
            return document.add_invite(user)
        if validated_data['document_permission'] == 'can_create':
            return document.add_create(user)
        if validated_data['document_permission'] == 'can_manage':
            return document.add_manage(user)

        raise ValidationError('Could not parse the document permission')
