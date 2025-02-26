from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token["email"] = user.email
        return token
            
class BuyerSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta: 
        model = CustomUser
        fields = ['id', 'url', 'image', 'username', 'email', 'role', 'phone', 'address']
        extra_kwargs = {
            'url': {'view_name': 'buyer-detail', 'lookup_field': 'pk'}
        }

        def create(self, validated_data):
            user = CustomUser.objects.create(**validated_data)
            return user
        
class SellerSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'image', 'username', 'email', 'role', 'phone', 'address']
        extra_kwargs = {
            'url': {'view_name': 'seller-detail', 'lookup_field': 'pk'}
        }

        def create(self, validated_data):
            user = CustomUser.objects.create(**validated_data)
            return user

class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True) 

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role', 'phone', 'address', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'default': False}
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            is_verified=validated_data['is_verified'],
        )
        return user