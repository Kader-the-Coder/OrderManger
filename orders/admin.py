from django.contrib import admin
from .models import Order, Product, OrderItem

admin.site.site_header = 'Order Manager'

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
