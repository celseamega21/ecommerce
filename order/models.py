from django.db import models
from account.models import CustomUser, Address
from product.models import Products
from cart.models import Cart
from django.core.exceptions import ValidationError

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('CC', 'Credit_Card'),
        ('bank_transfer', 'Bank Transer'),
        ('ewallet', 'E-Wallet'),
        ('COD', 'Cash on Delivery'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    method = models.CharField(choices=PAYMENT_CHOICES, max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.method}"
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('delivered', 'Delivered'),
        ('refund', 'Refund'),
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(choices=STATUS_CHOICES, max_length=16)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    notes = models.CharField(max_length=120)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} {self.quantity} pcs"
    
    def validate_quantity(self):
        if self.quantity > self.product.stock:
            raise ValidationError(f"Only {self.product.stock} left in stock.")
        