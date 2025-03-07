from rest_framework import serializers
from .models import *
from cart.models import Cart
from account.models import CustomUser
from django.utils import timezone

class PaymentsSerializers(serializers.ModelField):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Payment
        fields = ['user', 'method']

class OrderItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    price = serializers.IntegerField(source='product.price', read_only=True)
    discount_price = serializers.IntegerField(source='product.discount', read_only=True)
    payment = serializers.CharField(source='payment.method', read_only=True)
    payment_method = serializers.CharField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'product_name', 'product_image', 'quantity', 'price', 'discount_price', 'payment', 'payment_method']
        read_only_fields = ['id', 'price']

class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True)
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    shipping_address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['cart', 'items', 'status', 'shipping_address', 'total_price', 'notes', 'created_at']
        read_only_fields = ['id', 'buyer', 'created_at']

    def get_total_price(self, obj):
        return sum((item.product.price - item.product.discount) * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        """
        Create new orders based on user cart data (checkout)
        """
        items_data = validated_data.pop('items')
        cart = validated_data.pop("cart")
        shipping_address = validated_data.pop("shipping_address")
        
        # Make new order
        order = Order.objects.create(cart=cart, shipping_address=shipping_address, **validated_data)

        total_price = 0
        order_items = []

        for item in items_data:
            print(f"item: {item}")
            product_data = item.get('product', {})
            product_id = product_data.get('id')
            quantity = item["quantity"]
            payment_method = item.pop("payment_method")

            try:
                product =  Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                raise serializers.ValidationError({"error": f"Product with ID {product_id} does not exist."})
            
            try:
                payment = Payment.objects.get(method=payment_method)
            except Payment.DoesNotExist:
                raise serializers.ValidationError({"error": f"Payment method {payment_method} not found"})

            if quantity > product.stock:
                raise serializers.ValidationError({"error": f"Stock not enough for {product.name}. Only {product.stock} stock left available."})

            product.stock -= quantity
            product.save()

            order_items.append(OrderItem(order=order, product=product, quantity=quantity, payment=payment))

            total_price += product.price * quantity

        # Save all OrderItems at once
        OrderItem.objects.bulk_create(order_items)

        # Update total price in order
        order.total = total_price
        order.save()

        return order

    def update(self, instance, validated_data):
        """
        Update an order if it's still awaiting payment
        """
        if instance.status != 'awaiting_payment':
            raise serializers.ValidationError({"error": "The order has been processed and cannot be updated."})
        
        items_data = validated_data.pop('items', None)

        # Update the other field in instance order
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # if items updated, check stock and recalculate total price
        if items_data:
            total_price = 0
            order_items = []

            for item in items_data:
                product = item["product"]
                quantity = item["quantity"]

                if quantity > product.stock:
                    raise serializers.ValidationError({"error": f"Stock not enough for {product.name}. Only {product.stock} stock left available."})
                    
                product.stock -= quantity
                product.save()

                order_items.append(OrderItem(order=instance, product=product, quantity=quantity))

                total_price += quantity * product.price

            # Delete all old OrderItem and create new ones
            instance.itens.all().delete()
            OrderItem.objects.create(order_items)

            instance.total = total_price

        instance.save()
        return instance
    
    def destroy(self, instance):
        """
        Delete an order if it's still waiting for payment (hasn't been processed)
        """

        if instance.status != 'awaiting_payment':
            raise serializers.ValidationError({"error": "The order has been processed and cannot be deleted."})

        instance.delete()
        return {"success": "Order deleted successfully."}
    
    def validate(self, attrs):
        items = attrs.get("items", [])

        if not items:
            raise serializers.ValidationError({"error": "At least one item is required in the order."})

        for item in items:
            product_data = item.get('product', {})
            product_id = product_data.get("id")
            
            try:
                product =  Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                raise serializers.ValidationError({"error": f"Product with ID {product_id} does not exist."})

            quantity = item.get("quantity")

            if not quantity or quantity <= 0:
                raise ValidationError({"error": "Quantity must be greater than 0."})

            if quantity > product.stock:
                raise serializers.ValidationError({"error": f"Stock not enough for {product.name}\nOnly {product.stock} stock left available."})

        return attrs