from rest_framework import viewsets, permissions, views, status
from .serializers import (CategorySerializers, SubCategorySerializers, StoreSerializers, 
                          ProductsSerializers, ProductReviewSerializers, WishlistSerializers)
from ecommerce import permissions as custom_permissions
from .models import Category, SubCategory, Store, Products, ProductReview, Wishlist
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.response import Response
from decimal import Decimal
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

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

# class SearchProduct(views.APIView):
#     def get(self, request):
#         # Take parameter from request
#         search_query = request.query_params.get('search', '')
#         category_id = request.query_params.get('category', '')
#         min_price = request.query_params.get('min_price', '')
#         max_price = request.query_params.get('max_price', '')
#         store = request.query_params.get('store', '')
#         page_number = int(request.query_params.get('page', 1))
#         items_per_page = int(request.query_params.get('limit', 10))

#         # Base queryset
#         products = Products.objects.filter(status='AVAILABLE')

#         # Apply filters
#         if search_query:
#             products = products.filter(
#                 Q(name__icontains=search_query) |
#                 Q(description__icontains=search_query)
#                 ) 
#         if category_id:
#             category_id = int(category_id)
#             products = products.filter(Q(category_id=category_id))
#         if store:
#             products = products.filter(Q(store__name__icontains=store))

#         # Price range filtering
#         if min_price:
#             products = products.filter(Q(price__gte=Decimal(min_price)))
#         if max_price:
#             products = products.filter(Q(price__lte=Decimal(max_price)))

#         # Order by
#         products = products.order_by('-created_at')

#         if not products.exists():
#             return Response({
#                 'data': [],
#                 'message': 'No products found matching'
#             }, status=status.HTTP_200_OK)

#         # Pagination
#         paginator = Paginator(products, per_page=items_per_page)
#         page_obj = paginator.get_page(page_number)

#         # Serializers
#         serializer = ProductsSerializers(page_obj, many=True, context={'request': request})

#         return Response({
#             'data': serializer.data,
#             'pagination': {
#                 'total': paginator.count,
#                 'totalPages': paginator.num_pages,
#                 'currentPage': page_obj.number,
#                 'limit': items_per_page
#             }
#         }, status=status.HTTP_200_OK)