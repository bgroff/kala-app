from rest_framework import serializers
from accounts.models import User
from documents.models import Document, DocumentVersion
from projects.models import Category, Project


class DocumentSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super(DocumentSerializer, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        if validated_data['version'] == 1:
            document = Document.objects.create(
                project=validated_data['project'],
                name=validated_data['name'],
                date=validated_data['created'],
            )
            if 'category' in validated_data.keys():
                document.category = validated_data['category']
                document.save()
        else:
            document = Document.objects.get(pk=validated_data['collection'])

        DocumentVersion.objects.create(
            document=document,
            url=validated_data['url'],
            size=validated_data['size'],
            created=validated_data['created'],
            person=validated_data['person'],
            name=validated_data['name'],
            description=validated_data['description']
        )
        return document

    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    size = serializers.IntegerField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    person = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created = serializers.DateTimeField()
    url = serializers.URLField()
    version = serializers.IntegerField()
    collection = serializers.IntegerField()

    def validate_project(self, project):
        if self.project.pk != project.pk:
            raise serializers.ValidationError('The project primary key cannot be different from the current project')
        return project
