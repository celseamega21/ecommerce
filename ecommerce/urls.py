from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/logout/', views.LogOutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
