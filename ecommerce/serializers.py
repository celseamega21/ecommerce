from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token["email"] = user.email

        return token
    
class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'url', 'username', 'email']
        extra_kwargs = {
            'url': {'view_name': 'user-detail', 'lookup_field': 'pk'}
        }

        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user
        
class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user