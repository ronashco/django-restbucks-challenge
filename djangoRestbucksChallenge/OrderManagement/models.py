from __future__ import unicode_literals
from CoffeeShop.models import Customer
from django.db import models
from datetime import datetime


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


class Order(models.Model):
    status = models.CharField(choices=(('waiting', 'waiting'), ('preparation', 'preparation'), ('ready', 'ready'),
                                       ('delivered', 'delivered')), max_length=20, default='waiting')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(choices=(('coffeeshop', 'inshop'), ('home', 'takeaway')), max_length=10)
    order_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.pk)


class OrderLine(models.Model):
    customized_product = models.ForeignKey(CustomizedProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
