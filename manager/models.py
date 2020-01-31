from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    price =  models.IntegerField()
    def __str__(self):
        return self.name




class Customer(models.Model):
    name = models.CharField(max_length=40)
    customer_email = models.EmailField()
    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product)
    customer = models.ForeignKey(Customer,null=True)

    WAITING = 'WA'
    PREPARATION = 'PR'
    READY = 'RD'
    DELIVERED = 'DV'
    STATUS_CHOICES = (
        (WAITING, 'waiting'),
        (PREPARATION, 'preparation'),
        (READY, 'ready'),
        (DELIVERED, 'delivered'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=WAITING,
    )

    TAKEAWAY = 'TA'
    INSHOP = 'IS'
    CONSUME_LOCATION_CHOICES = (
        (TAKEAWAY , 'take away'),
        (INSHOP, 'in shop'),
    )
    consume_location = models.CharField(
        max_length=2,
        choices=CONSUME_LOCATION_CHOICES,
        default=INSHOP,
    )
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.status


class Option(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name


class Varient(models.Model):
    order = models.ForeignKey(Option)
    name = models.CharField(max_length=40)
    # order_item = models.ManyToManyRel(Order_item)
    def __str__(self):
        return self.name


class Order_item(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    varient = models.ManyToManyField(Varient)
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name


