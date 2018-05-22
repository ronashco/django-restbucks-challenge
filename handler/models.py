from django.db import models
from django.contrib.auth.models import User


class OrderStatus(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Product(models.Model):
    product = models.CharField(max_length=200)

    def __str__(self):
        return self.product


class Place(models.Model):
    place = models.CharField(max_length=200)

    def __str__(self):
        return self.place


class Order(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    consume_place = models.ForeignKey(Place)
    option = models.CharField(max_length=30)
    status = models.ForeignKey(OrderStatus)

    def __str__(self):
        return str(self.id)
