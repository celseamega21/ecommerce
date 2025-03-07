from django.db import models
from account.models import CustomUser
from product.models import Products
from django.core.exceptions import ValidationError

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    @property
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    # @property
    # def price(self):
    #     return self.product.price
    
    def validate_quantity(self):
        if self.quantity > self.product.stock:
            raise ValidationError(f"Only {self.product.stock} left in stock")

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"