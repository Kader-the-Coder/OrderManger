from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='owned_companies')
    members = models.ManyToManyField('CustomUser', related_name='companies')

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    def __str__(self):
        return self.username
