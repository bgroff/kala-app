from rest_framework import serializers
from documents.models import DocumentPermission


class DocumentPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    document_id = serializers.IntegerField()
    project_id = serializers.IntegerField()
    organization_id = serializers.IntegerField()
    document_permission = serializers.CharField()
    project_permission = serializers.CharField()
    organization_permission = serializers.CharField()
