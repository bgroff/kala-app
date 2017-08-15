from rest_framework import serializers
from organizations.models import Organization


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id', 'uuid', 'name', 'website', 'phone', 'fax',
            'address', 'address1', 'city', 'state', 'zip',
            'country', 'timezone'
        ]

    def create(self, validated_data):
        return Organization.objects.create(**validated_data)

    def validate_name(self, value):
        # At least try to dedup names
        if Organization.objects.filter(name__iexact=value):
            raise serializers.ValidationError('Name is already in use.')
        return value
