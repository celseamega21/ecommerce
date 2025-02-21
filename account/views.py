from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser
from .serializers import UserAllSerializers

class UserAllViewSet(viewsets.ModelViewSet):
    queryset =  CustomUser.objects.all()
    serializer_class = UserAllSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]