from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'users', views.UserAllViewSet, basename='user')
router.register(r'buyers', views.BuyerViewSet, basename='buyer')
router.register(r'sellers', views.SellerViewSet, basename='seller')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('api/register/buyer/', views.BuyerRegisterView.as_view(), name='buyer_register'),
    path('api/register/seller/', views.SellerRegisterView.as_view(), name='seller_register'),
    path('api/logout/', views.LogOutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
