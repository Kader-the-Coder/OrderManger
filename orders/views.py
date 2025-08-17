from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from .models import Order, Product, OrderItem
from decimal import Decimal


def index(request):
    return render(request, "index.html")


@require_GET
def display_orders(request):
    all_orders = Order.objects.all().prefetch_related("items__product")
    all_products = Product.objects.all()
    context = {
        "orders": all_orders,
        "products": all_products,
    }
    return render(request, "orders.html", context)


@require_POST
def create_order(request):
    """
    Create a new order with its items.

    Expects POST data:
        name (str): Customer name
        block (int): Block number
        unit (int): Unit number
        product_<id> (int): Quantity for each product
    """
    # Extract order fields from POST data
    name = request.POST.get("name")
    block = request.POST.get("block")
    unit = request.POST.get("unit")

    if name and block and unit:
        try:
            order = Order.objects.create(
                name=name,
                block=int(block),
                unit=int(unit)
            )

            # Loop through POST items to create OrderItems
            for key, value in request.POST.items():
                if key.startswith("product_") and value:
                    product_id = key.replace("product_", "")
                    try:
                        product = Product.objects.get(id=int(product_id))
                        quantity = int(value)
                        if quantity > 0:
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity
                            )
                    except Product.DoesNotExist:
                        continue

        except ValueError:
            pass  # optionally handle invalid block/unit numbers

    # Redirect to order list after creation
    return redirect("orders:display_orders")  # replace with your URL name


@require_POST
def create_product(request):
    """
    Create a new product.

    Expects POST data:
        name (str): Product name
        price (Decimal): Product price
    """
    name = request.POST.get("name")
    price = request.POST.get("price")

    if name and price:
        try:
            price_decimal = Decimal(price)
            Product.objects.create(name=name, price=price_decimal)
        except ValueError:
            pass  # optionally handle invalid price

    return redirect("orders:display_products")  # Replace with your URL name for listing products


@require_POST
def delete_product(request, product_id: int):
    """
    Delete a product by its ID.
    """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('orders:display_products')


@require_GET
def display_products(request):
    """
    List all existing products.
    """
    all_products = Product.objects.all()
    context = {"products": all_products}
    return render(request, "products.html", context)
