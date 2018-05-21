from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class OrderStatus(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Product(models.Model):
    product = models.CharField(max_length=200)

    def __str__(self):
        return self.product


class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    consume_place = models.CharField(max_length=30)
    option = models.CharField(max_length=30)
    status = models.ForeignKey(OrderStatus)

    def __str__(self):
        return self.id
