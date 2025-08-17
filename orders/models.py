from django.db import models
from decimal import Decimal


class Order(models.Model):
    """
    Represents a customer order with associated order items.

    Attributes:
        name (str): Name of the customer placing the order.
        block (int): Block number of the customer.
        unit (int): Unit number of the customer.
        created_at (datetime): Timestamp when the order was created.
        updated_at (datetime): Timestamp when the order was last updated.

    Properties:
        total_price (Decimal): Total cost of all items in the order.
    """
    name = models.CharField(max_length=100)
    block = models.IntegerField()
    unit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} (Block {self.block}, Unit {self.unit})"

    @property
    def total_price(self) -> Decimal:
        """Compute the total price of all order items."""
        return sum((item.total_price for item in self.items.all()), Decimal('0'))


class Product(models.Model):
    """
    Represents a product that can be ordered.

    Attributes:
        name (str): Name of the product.
        price (Decimal): Price of the product.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} (R{self.price})"


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

    def __str__(self) -> str:
        return f"{self.product.name}: {self.quantity}"

    @property
    def total_price(self) -> Decimal:
        """Compute the total price for this order item."""
        return Decimal(self.quantity) * self.product.price
