from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .models import Order, Product, OrderItem
from decimal import Decimal
from accounts.decorators import company_required


def index(request):
    return render(request, "index.html")


@login_required
@require_GET
@company_required
def display_orders(request):
    company = request.user.company
    all_orders = Order.objects.filter(company=company).prefetch_related("items__product")
    available_products = Product.objects.filter(discontinued=False, company=company)
    
    context = {
        "orders": all_orders,
        "products": available_products,
    }
    return render(request, "orders.html", context)



@login_required
@require_POST
@company_required
def create_order(request):
    """
    Create a new order with its items.
    """
    company = request.user.company

    name = request.POST.get("name")
    block = request.POST.get("block")
    unit = request.POST.get("unit")

    if name and block and unit:
        try:
            order = Order.objects.create(
                name=name,
                block=int(block),
                unit=int(unit),
                company=company
            )

            # Loop through POST items to create OrderItems
            for key, value in request.POST.items():
                if key.startswith("product_") and value:
                    product_id = key.replace("product_", "")
                    try:
                        product = Product.objects.get(id=int(product_id), discontinued=False, company=company)
                        quantity = int(value)
                        if quantity > 0:
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity
                            )
                    except Product.DoesNotExist:
                        continue  # skip discontinued or invalid products

        except ValueError:
            pass  # optionally handle invalid block/unit numbers

    return redirect("orders:display_orders")


@login_required
@require_POST
@company_required
def update_order(request, order_id):
    company = request.user.company
    order = get_object_or_404(Order, id=order_id, company=company)

    # Update basic fields
    order.name = request.POST.get("name", order.name)
    order.block = int(request.POST.get("block", order.block))
    order.unit = int(request.POST.get("unit", order.unit))
    order.save()  # updates updated_at

    # Update quantities for existing items or create new OrderItems
    for key, value in request.POST.items():
        if key.startswith("product_"):
            product_id = int(key.replace("product_", ""))
            quantity = int(value)
            product = get_object_or_404(Product, id=product_id, company=company)

            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if quantity > 0:
                order_item.quantity = quantity
                order_item.save()
            else:
                if not created:
                    order_item.delete()

    order.save()
    return redirect("orders:display_orders")


@login_required
@require_POST
@company_required
def delete_order(request, order_id):
    company = request.user.company
    order = get_object_or_404(Order, id=order_id, company=company)
    order.delete()
    return redirect("orders:display_orders")


@login_required
@require_POST
@company_required
def toggle_order_status(request, order_id):
    company = request.user.company
    order = get_object_or_404(Order, id=order_id, company=company)
    new_status = request.POST.get("status")
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
    return redirect("orders:display_orders")


@login_required
@require_POST
@company_required
def toggle_order_payment(request, order_id):
    company = request.user.company
    order = get_object_or_404(Order, id=order_id, company=company)
    new_payment_status = request.POST.get("payment_status")
    if new_payment_status in dict(Order.PAYMENT_CHOICES):
        order.payment_status = new_payment_status
        order.save()
    return redirect("orders:display_orders")


@login_required
@require_POST
@company_required
def create_product(request):
    """
    Create a new product tied to the logged-in user's company.
    """
    company = request.user.company
    name = request.POST.get("name")
    price = request.POST.get("price")

    if name and price:
        price_decimal = Decimal(price)
        Product.objects.create(name=name, price=price_decimal, company=company)

    return redirect("orders:display_products")


@login_required
@require_POST
@company_required
def delete_product(request, product_id: int):
    """
    Delete a product if it is not in any active order.
    Otherwise, mark it as discontinued.
    """
    company = request.user.company
    product = get_object_or_404(Product, id=product_id, company=company)

    in_orders = OrderItem.objects.filter(product=product, order__company=company, quantity__gt=0).exists()

    if in_orders:
        product.discontinued = True
        product.save()
    else:
        product.delete()

    return redirect("orders:display_products")


@login_required
@require_GET
@company_required
def display_products(request):
    """
    List products for the logged-in user's company and mark which ones are actively used in orders (quantity > 0).
    """
    company = request.user.company
    all_products = Product.objects.filter(company=company)

    product_ids_in_active_orders = set(
        OrderItem.objects.filter(order__company=company, quantity__gt=0).values_list("product_id", flat=True)
    )

    context = {
        "products": all_products,
        "product_ids_in_active_orders": product_ids_in_active_orders,
    }
    return render(request, "products.html", context)


@login_required
@require_POST
@company_required
def toggle_discontinue_product(request, product_id):
    """
    Toggle the discontinued status of a product.
    """
    company = request.user.company
    product = get_object_or_404(Product, id=product_id, company=company)
    product.discontinued = not product.discontinued
    product.save()
    return redirect("orders:display_products")
