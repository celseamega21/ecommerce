from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CartSerializers
from cart.models import Cart, Products, CartItem
from rest_framework.response import Response
from rest_framework.decorators import action

class CartViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializers

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def get_or_create_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def list(self, request):
        """
        GET api/cart/
        get cart's user
        """
        cart = self.get_or_create_cart()
        serializer = self.get_serializer(cart)
        return Response(serializer.data) 
    
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """
        GET api/cart/add_item/
        Add item to cart
        """
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity'))

        if not product_id or quantity is None:
            return Response(
                {'error': 'Product ID and quantity is required'},
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
                )
 
        cart = self.get_or_create_cart()

        # Check if product available in cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                            product=product,
                                                            defaults={'price': product.price, 'quantity': quantity})
        
        # Total items already in cart
        existing_quantity = cart_item.quantity if not created else 0

        available_stock = product.stock - existing_quantity

        if created:
            cart_item.quantity = quantity
        else:
            if cart_item.quantity + quantity > product.stock:
                return Response({'error': f'Maximum stock available: {available_stock}'},
                                status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()

        return Response(self.get_serializer(cart).data)
    
    @action(detail=False, methods=["put"])
    def update_item(self, request):
        """
        PUT api/cart/update_item/
        Update quantity of cart item
        """
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))

        if not item_id or quantity is None:
            return Response(
                {'error': 'Product ID and quantity is required'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        cart = self.get_or_create_cart()

        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        product = cart_item.product

        if cart_item.quantity + quantity > product.stock:
            return Response({'error': f'Maximum stock available: {product.stock}'},
                status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        return Response(self.get_serializer(cart).data)
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """
        DELETE api/cart/remove_item/
        Remove item from cart
        """
        item_id = request.data.get('item_id')

        if not item_id:
            return Response(
                {'error': 'Item ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = self.get_or_create_cart()

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(self.get_serializer(cart).data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """
        POST api/cart/clear/
        Empty the cart
        """
        cart = self.get_or_create_cart()
        cart.items.all().delete()

        return Response(self.get_serializer(cart).data)