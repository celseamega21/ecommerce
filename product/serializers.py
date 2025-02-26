from rest_framework import serializers
from .models import Category, SubCategory, Store, Products, ProductReview, Wishlist
from account.serializers import CustomUserSerializers
from account.models import CustomUser

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = SubCategory
        fields = ['category', 'subcategory']

class StoreSerializers(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(source='owner.username')
    logo = serializers.ImageField(use_url=True)

    class Meta:
        model = Store
        fields = ['id', 'url', 'name', 'description', 'owner', 'logo', 'created_at', 'updated_at']
        extra_kwargs = {
            'url': {'view_name': 'store-detail', 'lookup_field': 'slug'}
        }

class ProductsSerializers(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)
    store = serializers.CharField(source='store.name')
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'url', 'name', 'image', 'store', 'product_detail']
        extra_kwargs = {
            'url': {'view_name': 'products-detail', 'lookup_field': 'slug'}
        }

    def get_product_detail(self, obj):
        return {
            "price": obj.price - obj.discount,
            "status": obj.status,
            "stock": obj.stock,
            "category": obj.category.name,
            "subcategory": obj.subcategory.subcategory,
            "weight": obj.weight,
            "description": obj.description,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }
        
class WishlistProductSerializers(serializers.ModelSerializer):
    store = serializers.StringRelatedField()

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
    user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    product = WishlistProductSerializers(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset = Products.objects.all(),
        many=True,
        write_only=True,
        source='product'
    )

    class Meta:
        model = Wishlist
        fields = ['user', 'product', 'product_ids']