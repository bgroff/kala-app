from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'company'
        ]

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def validate_name(self, value):
        # At least try to dedup names
        if Project.objects.filter(name__iexact=value):
            raise serializers.ValidationError('Name is already in use.')
        return value
