from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CustomizedProduct(models.Model):
    product = models.ForeignKey(Product)
    option = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.product) + ' --> ' + self.option + ' : ' + self.type


