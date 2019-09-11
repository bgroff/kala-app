from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from organizations.models import OrganizationPermission
from django.contrib.auth import get_user_model

User = get_user_model()


class OrganizationPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=True)
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    permission = serializers.ChoiceField(required=True,
                                                  choices=[('can_invite', 'Can invite'),
                                                           ('can_create', 'Can create'),
                                                           ('can_manage', 'Can manage'),
                                                           ('canInvite', 'Can invite'),
                                                           ('canCreate', 'Can create'),
                                                           ('canManage', 'Can manage')])

    def to_representation(self, obj):
        if type(obj) == OrganizationPermission:
            return self.from_organization_permission(obj)
        else:
            return self.from_record(obj)

    def from_organization_permission(self, obj):
        representation = {
            'organization': {
                'id': obj.id,
                self.format_permission(obj.permission.codename): True
            }
        }

        return representation

    def from_record(self, obj):
        representation = {
            'user': {
                'id': obj.user_id,
                'username': obj.username,
                'firstName': obj.first_name,
                'lastName': obj.last_name
            }
        }
        if obj.organization_permission:
            representation['organization'] = {
                self.format_permission(obj.organization_permission): True
            }
        return representation

    def format_permission(self, obj):
        permission = obj.split('_')
        permission = "{0}{1}".format(permission[0], permission[1].capitalize())
        return permission

    # These need to check that the user in the payload is available to
    # the user making the request.
    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        organization = self.context.get('organization')
        if validated_data['permission'] == 'canInvite':
            return organization.add_invite(user)
        if validated_data['permission'] == 'canCreate':
            return organization.add_create(user)
        if validated_data['permission'] == 'canManage':
            return organization.add_manage(user)

        raise ValidationError('Could not parse the document permission')

    def update(self, instance, validated_data):
        user = User.objects.get(id=validated_data['user_id'])
        organization = self.context.get('organization')
        if validated_data['permission'] == 'canInvite':
            return organization.add_invite(user)
        if validated_data['permission'] == 'canCreate':
            return organization.add_create(user)
        if validated_data['permission'] == 'canManage':
            return organization.add_manage(user)

        instance.refresh_from_db()
        return instance
