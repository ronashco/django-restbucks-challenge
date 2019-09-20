from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import signals

"""
status of a order which can modify by admin
"""


class OrderStatus(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


"""
model of products that served in coffee shop
"""


class Product(models.Model):
    product = models.CharField(max_length=200)

    def __str__(self):
        return self.product


"""
model of places that a customer can eat his product
"""


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


"""
this method sends email to owner of a order whenever a status for order changed
"""


@receiver(pre_save, sender=Order, dispatch_uid='status')
def active(sender, instance, **kwargs):
    if instance is None:
        return;
    subject = 'Status Changed'
    message = 'dear %s one of your orders status may be change please refresh the home page' % instance.user.username
    from_email = settings.EMAIL_HOST_USER
    print(from_email)
    send_mail(subject, message, from_email, [instance.user.username], fail_silently=False)
