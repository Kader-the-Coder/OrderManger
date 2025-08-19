from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", views.display_orders, name="display_orders"),
    path("orders/create/", views.create_order, name="create_order"),
    path("orders/update/<int:order_id>/", views.update_order, name="update_order"),
    path("orders/delete/<int:order_id>/", views.delete_order, name="delete_order"),
    path("orders/toggle_order_status/<int:order_id>/", views.toggle_order_status, name="toggle_order_status"),
    path("orders/toggle_order_payment/<int:order_id>/", views.toggle_order_payment, name="toggle_order_payment"),
    path("products/", views.display_products, name="display_products"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/toggle_discontinue/<int:product_id>/", views.toggle_discontinue_product, name="toggle_discontinue_product"),
    path("products/delete/<int:product_id>/", views.delete_product, name="delete_product"),
]
