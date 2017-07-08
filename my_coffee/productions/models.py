from django.db import models


class Menu(models.Model):
    name = models.CharField()
    options = models.ManyToManyField(ProductOption)
    price = models.IntegerField(default=0)


class ProductOption(models.Model):
    name = models.CharField()
    detail_option = models.ManyToManyField(DetailOption)


class DetailOption(models.Model):
    name = models.CharField()
    price = models.IntegerField(default=0)