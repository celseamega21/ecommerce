from rest_framework import serializers
from .models import Category, SubCategory, Store, Products, ProductReview, Wishlist
from account.serializers import CustomUserSerializers

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializers(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = SubCategory
        fields = ['category', 'name']

class StoreSerializers(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='customuser.username')
    logo = serializers.ImageField(use_url=True)

    class Meta:
        model = Store
        fields = ['id', 'url', 'name', 'description', 'owner', 'logo', 'created_at', 'updated_at']
        extra_kwargs = {
            'url': {'view_name': 'store-detail', 'lookup_field': 'slug'}
        }

class ProductsSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)
    store = serializers.CharField(source='store-detail')
    category = CategorySerializers()
    subcategory = SubCategorySerializers()
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'url', 'name', 'image', 'store', 'product_detail']
        extra_kwargs = {
            'url': {'view_name': 'products-detail', 'lookup_field': 'slug'}
        }

        def get_product_detail(self, obj):
            return {
                "price": obj.price,
                "status": obj.status,
                "stock": obj.stock,
                "category": obj.category.name,
                "subcategory": obj.subcategory.name,
                "weight": obj.weight,
                "description": obj.description,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
            }
        
class WishlistProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'store', 'status', 'stock']
        
class ProductReviewSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source='products-detail')
    user = CustomUserSerializers(read_only=True)
    
    class Meta:
        model = ProductReview
        fields = ['user', 'product_name', 'rating', 'review', 'created_at']

class WishlistSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source='customuser-detail')
    product = WishlistProductSerializers(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['user', 'product']