from django.contrib import admin
from .models import CompanyInvitation

admin.site.site_header = 'Order Manager'

# Register your models here.
admin.site.register(CompanyInvitation)
