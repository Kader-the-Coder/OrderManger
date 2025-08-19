from django.db import models
from decimal import Decimal


# orders/models.py

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discontinued = models.BooleanField(default=False)
    company = models.ForeignKey(
        'accounts.Company',
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]
    PAYMENT_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ]

    name = models.CharField(max_length=100)
    block = models.IntegerField()
    unit = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        'accounts.Company',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return self.name



class OrderItem(models.Model):
    """
    Represents an individual product within an order.

    Attributes:
        order (ForeignKey[Order]): The order this item belongs to.
        product (ForeignKey[Product]): The product being ordered.
        quantity (int): Quantity of the product in the order.

    Properties:
        total_price (Decimal): Total price for this item (quantity * product price).
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def total_price(self) -> Decimal:
        """Compute the total price for this order item."""
        return Decimal(self.quantity) * self.product.price

    def __str__(self) -> str:
        return f"{self.product.name}: {self.quantity}"
