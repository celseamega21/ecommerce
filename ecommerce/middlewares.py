from django.urls import reverse
from django.contrib.auth import logout

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        response = self.get_response(request)
        return response
    
class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('logout'):
            logout(request)
        
        response = self.get_response(request)
        return response 