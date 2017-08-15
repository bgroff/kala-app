from rest_framework import serializers
from projects.models import Project, Category


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'organization'
        ]

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def validate_name(self, value):
        # At least try to dedup names
        if Project.objects.filter(name__iexact=value):
            raise serializers.ValidationError('Name is already in use.')
        return value


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(CategorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'type', 'project'
        ]

    def validate_project(self, project):
        if self.project.pk != project.pk:
            raise serializers.ValidationError('The project primary key cannot be different from the current project')
        return project

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
