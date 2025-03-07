from rest_framework import viewsets, permissions, generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CustomUser, Address
from .serializers import UserAllSerializers, UserRegistrationSerializers, BuyerSerializers, SellerSerializers, AddressSerializers
from rest_framework.response import Response

class UserAllViewSet(viewsets.ModelViewSet):
    queryset =  CustomUser.objects.all()
    serializer_class = UserAllSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class BuyerRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='BUYER')

        return Response({"message": "Account for buyer has been successfully registered"},
                        status=status.HTTP_201_CREATED)

class SellerRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='SELLER')

        return Response({"message": "Account for seller has been successfully resgistered"}, 
                        status=status.HTTP_201_CREATED)
    
class BuyerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role='BUYER')
    serializer_class = BuyerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class SellerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role='SELLER')
    serializer_class = SellerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)