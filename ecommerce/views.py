from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializers, UserSerializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User created successfully"},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
