from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email', 'username', 'avatar_url', 'date_joined')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_email(self, value):
        # At least try to dedup emails
        if User.objects.filter(email__iexact=value):
            raise serializers.ValidationError('Email address is already in use.')
        return value
