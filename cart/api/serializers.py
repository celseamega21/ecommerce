from rest_framework import serializers
from cart.models import Cart, CartItem

class CartItemSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_id = serializers.CharField(source='product.id')
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'product_image', 
                  'quantity', 'price', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'price', 'created_at', 'updated_at']

class CartSerializers(serializers.ModelSerializer):
    items = CartItemSerializers(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Cart
        fields = [ 'user', 'items', 'total_items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())