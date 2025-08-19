from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Company

admin.site.site_header = 'Order Manager'
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Company)
