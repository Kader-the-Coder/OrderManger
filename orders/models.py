from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=100)
    block = models.IntegerField()
    unit = models.IntegerField()
    chicken_samoosa_quantity = models.IntegerField()
    mince_samoosa_quantity = models.IntegerField()
    koeksister_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Block {self.block}, Unit {self.unit})"
