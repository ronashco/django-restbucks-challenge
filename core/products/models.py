from django.db import models
from django.contrib.postgres.fields import ArrayField


class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.IntegerField()
    option = models.CharField(max_length=250, null=True, blank=True, default=None)
    items = ArrayField(models.CharField(max_length=250), null=True, default=None)
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return self.title
