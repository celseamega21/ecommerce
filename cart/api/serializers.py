from rest_framework import serializers
from cart.models import Cart, CartItem

class CartItemSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_id = serializers.IntegerField(source='product.id')
    discount_price = serializers.IntegerField(source='product.discount', read_only=True)
    price = serializers.IntegerField(source='product.price', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'product_image', 
                  'quantity', 'price', 'discount_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price', 'created_at', 'updated_at']

class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'final_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_final_price(self, obj):
        return sum((item.product.price - item.product.discount) * item.quantity for item in obj.items.all())
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())    