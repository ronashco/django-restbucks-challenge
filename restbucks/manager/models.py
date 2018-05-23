from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


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


class Option(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=40)
    def __str__(self):
        return self.name


class Varient(models.Model):
    option = models.ForeignKey(Option, null=True)
    name = models.CharField(max_length=40)
    # order_item = models.ManyToManyRel(Order_item)
    def __str__(self):
        return self.name




class Order(models.Model):

    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=('owner'), null=True)
    product = models.ForeignKey(Product)
    customer = models.ForeignKey(Customer, null=True)

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
    (TAKEAWAY, 'take away'),
    (INSHOP, 'in shop'),
    )
    consume_location = models.CharField(
        max_length=2,
        choices=CONSUME_LOCATION_CHOICES,
        default=INSHOP,
    )
    varient = models.ForeignKey(Varient, null=True)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.customer.name


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.status != self.__original_status:
            send_mail('Your order status has changed!', self.status , 'Manager@restbucks.co',
                      [self.customer.customer_email])


    # name changed - do something here

# class Order_item(models.Model):
#     product = models.ForeignKey(Product)
#     order = models.ForeignKey(Order)
#     varient = models.ManyToManyField(Varient)



