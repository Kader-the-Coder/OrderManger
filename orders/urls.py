from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", views.display_orders, name="display_orders"),
    path("orders/create/", views.create_order, name="create_order"),
    path("products/", views.display_products, name="display_products"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),
]