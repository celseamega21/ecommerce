from rest_framework import viewsets, permissions, views, status
from .serializers import (CategorySerializers, SubCategorySerializers, StoreSerializers, 
                          ProductsSerializers, ProductReviewSerializers, WishlistSerializers)
from ecommerce import permissions as custom_permissions
from product.models import Category, SubCategory, Store, Products, ProductReview, Wishlist
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [custom_permissions.IsAdminOrSeller]
    authentication_classes = [JWTAuthentication]

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [custom_permissions.IsAdminOrSeller]
    authentication_classes = [JWTAuthentication]
        
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializers
    permission_classes = [custom_permissions.IsAdminOrSeller]
    authentication_classes = [JWTAuthentication]
    lookup_field = 'slug'

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
    permission_classes = [custom_permissions.IsAdminOrSeller or permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    lookup_field = 'slug'

class ProductReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializers
    permission_classes = [permissions.AllowAny]

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
