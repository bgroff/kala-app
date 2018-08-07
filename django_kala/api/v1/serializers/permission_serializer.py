from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers

from auth.models import Permissions

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['user', 'permission', 'object_uuid']
