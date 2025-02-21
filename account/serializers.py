from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()

class UserAllSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'image', 'username', 'email', 'role', 'phone', 'address']
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'pk'}
        }

        def create(self, validated_data):
            user = CustomUser.objects.create(**validated_data)
            return user

class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role']