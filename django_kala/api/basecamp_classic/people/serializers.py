from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'username',
            'avatar_url', 'date_joined', 'is_active', 'is_admin',
            'organizations'
        )

    def create(self, validated_data):
        companies = validated_data.pop('companies')
        user = User.objects.create(**validated_data)
        user.organizations.add(*companies)
        return user
