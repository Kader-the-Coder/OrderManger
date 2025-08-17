from django.shortcuts import render
from .models import Order


def index(request):
    return render(request, "index.html")


def orders(request):
    if request.method == "POST":
        name = request.POST.get("name")
        block = request.POST.get("block")
        unit = request.POST.get("unit")
        chicken_samoosa_quantity = request.POST.get("chicken_samoosa_quantity")
        mince_samoosa_quantity = request.POST.get("mince_samoosa_quantity")
        koeksister_quantity = request.POST.get("koeksister_quantity")

        order = Order(
            name=name,
            block=block,
            unit=unit,
            chicken_samoosa_quantity=chicken_samoosa_quantity,
            mince_samoosa_quantity=mince_samoosa_quantity,
            koeksister_quantity=koeksister_quantity,
        )
        order.save()
    return render(request, "orders.html")
