from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
from account.views import UserAllViewSet as UserAccountViewSet
from product import views as v

router = DefaultRouter()
router.register(r'users', UserAccountViewSet, basename='user')
router.register(r'buyers', views.BuyerViewSet, basename='buyer')
router.register(r'sellers', views.SellerViewSet, basename='seller')
router.register(r'categorys', v.CategoryViewSet, basename='category')
router.register(r'subcategorys', v.SubCategoryViewSet, basename='subcategory')
router.register(r'stores', v.StoreViewSet, basename='store')
router.register(r'products', v.ProductsViewSet, basename='products')
router.register(r'product-reviews', v.ProductReviewViewSet, basename='product-review')
router.register(r'wishlists', v.WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('api/register/buyer/', views.BuyerRegisterView.as_view(), name='buyer_register'),
    path('api/register/seller/', views.SellerRegisterView.as_view(), name='seller_register'),
    path('api/logout/', views.LogOutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
