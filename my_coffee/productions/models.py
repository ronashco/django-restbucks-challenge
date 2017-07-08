from django.db import models


class DetailOption(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

class ProductOption(models.Model):
    name = models.CharField(max_length=50)
    detail_option = models.ManyToManyField(DetailOption)

class Menu(models.Model):
    name = models.CharField(max_length=50)
    options = models.ManyToManyField(ProductOption)
    price = models.IntegerField(default=0)

