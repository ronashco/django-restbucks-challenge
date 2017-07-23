from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUSES = (("W", "waiting"), ("P", "preparation"),
                ("R", "ready"))
    LOCATIONS = (("TA", "take away"), ("IS", "in shop"))
    owner = models.ForeignKey(User)
    status = models.CharField(max_length=1, choices=STATUSES,
                              default="W")
    location = models.CharField(max_length=2, choices=LOCATIONS,
                                default="IS")
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    ordered_productions = models.ManyToManyField("productions.Menu")


