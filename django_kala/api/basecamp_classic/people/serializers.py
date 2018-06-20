from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'username',
            'avatar_url', 'date_joined', 'is_active', 'is_superuser',
            'organizations'
        )

    def create(self, validated_data):
        organizations = validated_data.pop('organizations')
        user = User.objects.create(**validated_data)
        user.organizations.add(*organizations)
        return user
