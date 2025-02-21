from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializers, BuyerSerializers, SellerSerializers
from account.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                access_token = response.data.get('access')
                refresh_token = response.data.get('refresh')

                if access_token and refresh_token:
                    #set access token in HttpOnly cookie
                    response.set_cookie(
                        key="access_token",
                        value=access_token,
                        httponly=True,
                        secure=False, #set True if use HTTPS
                        samesite="Lax",
                        max_age=300,
                    )

                    #set access token in HttpOnly cookie
                    response.set_cookie(
                        key="refresh_token",
                        value=refresh_token,
                        httponly=True,
                        secure=False, #set True if use HTTPS
                        samesite="Lax", 
                        max_age=300
                    )

                    #Remove token from response body
                    del response.data['access']
                    del response.data['refresh']
                else:
                    return Response({'error': 'Tokens not found in response'},
                                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        except Exception as e:
            return Response({'error': f'Error during token creation: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']

            #Set new access token in HttpOnly cookie
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=300,
            )

            #Remove access token from response body
            del response.data['access']
        return response
    
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

class LogOutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception as e:
            return Response({'error': {str(e)}}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Logged out successfully"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    
class BuyerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role__iexact='BUYER')
    serializer_class = BuyerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

class SellerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(role__iexact='SELLER')
    serializer_class = SellerSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]