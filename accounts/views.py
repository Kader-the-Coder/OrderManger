from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Company
from django.contrib import messages
from django.db import transaction


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        name = request.POST.get("name")
        company_name = request.POST.get("company_name")

        if not username or not password1 or not password2 or not name:
            messages.error(request, "All fields are required.")
            return redirect("accounts:register")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("accounts:register")

        try:
            with transaction.atomic():
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password1,
                    name=name
                )
                company = Company.objects.create(
                    name=company_name,
                    owner=user
                )
                company.members.add(user)
                user.company = company
                user.save()
                login(request, user)
                return redirect("orders:index")
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect("accounts:register")

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("orders:index")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")
