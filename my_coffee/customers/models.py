from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUSES = (("W", "waiting"), ("P", "preparation"),
                ("R", "ready"))
    LOCATIONS = (("TA", "take away"), ("IS", "in shop"))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    status = models.CharField(max_length=1, choices=STATUSES,
                              default="W")
    price = models.IntegerField(default=0)
    location = models.CharField(max_length=2, choices=LOCATIONS,
                                default="IS")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    ordered_productions = models.ManyToManyField(OrderedProduction)


class OrderedProduction(models.Model):
    name = models.CharField()
    product = models.ManyToManyField("productions.Menu")
