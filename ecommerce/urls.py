from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import BuyerViewSet, SellerViewSet, BuyerRegisterView, SellerRegisterView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from account.views import UserAllViewSet as UserAccountViewSet, AddressViewSet
from product.views import CategoryViewSet, SubCategoryViewSet, StoreViewSet, ProductsViewSet, WishlistViewSet, ProductReviewViewSet
from rest_framework_simplejwt import views as tokenviews
from cart.api.views import CartViewSet
from order.views import OrderViewSet

router = DefaultRouter()
router.register(r'users', UserAccountViewSet, basename='user')
router.register(r'buyers', BuyerViewSet, basename='buyer')
router.register(r'sellers', SellerViewSet, basename='seller')
router.register(r'categorys', CategoryViewSet, basename='category')
router.register(r'subcategorys', SubCategoryViewSet, basename='subcategory')
router.register(r'stores', StoreViewSet, basename='store')
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'product-reviews', ProductReviewViewSet, basename='product-review')
router.register(r'wishlists', WishlistViewSet, basename='wishlist')
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', tokenviews.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', tokenviews.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/buyer/', BuyerRegisterView.as_view(), name='buyer_register'),
    path('api/register/seller/', SellerRegisterView.as_view(), name='seller_register'),
    path('api/logout/', views.LogOutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
