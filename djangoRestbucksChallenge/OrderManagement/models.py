from __future__ import unicode_literals
from CoffeeShop.models import Customer
from django.db import models
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_init, post_delete, post_save

#email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Product(models.Model):
    price = models.IntegerField(default=0)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Product, dispatch_uid="add None option")
def create_none_option(sender, instance, **kwargs):
    if CustomizedProduct.objects.filter(product=instance).count() == 0:
        CustomizedProduct.objects.create(product=instance, option='None', type='None')


class CustomizedProduct(models.Model):
    product = models.ForeignKey(Product)
    option = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

    def __str__(self):
        return str(self.product) + ' --> ' + self.option + ' : ' + self.type


@receiver(post_save, sender=CustomizedProduct, dispatch_uid="delete option")
def delete_none_option(sender, instance, **kwargs):
    if instance.option != 'None' and CustomizedProduct.objects.filter(product=instance.product, option='None').count() != 0:
        cp = CustomizedProduct.objects.filter(product=instance.product, option='None').first()
        if cp:
            cp.delete()


@receiver(post_delete, sender=CustomizedProduct, dispatch_uid="add option")
def add_none_option(sender, instance, **kwargs):
    if instance.option != 'None':
        count = CustomizedProduct.objects.filter(product=instance.product).count()
        if count == 0:
            CustomizedProduct.objects.create(product=instance.product, option='None', type='None')


class Order(models.Model):
    status = models.CharField(choices=(('waiting', 'waiting'), ('preparation', 'preparation'), ('ready', 'ready'),
                                       ('delivered', 'delivered')), max_length=20, default='waiting')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location = models.CharField(choices=(('coffeeshop', 'coffeeshop'), ('takeaway', 'takeaway')), max_length=10)
    order_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.pk)


def send_mail(server, rec, msg):
    server.starttls()
    server.login('childf2018@gmail.com', 'childf2018childf')
    mail = MIMEMultipart()
    mail['From'] = 'childf2018@gmail.com'
    mail['To'] = rec
    mail['Subject'] = 'change notification'
    mail.attach(MIMEText(msg, 'plain'))
    # server.send_message(mail, 'childf2018@gmail.com', rec)
    server.sendmail('childf2018@gmail.com', rec, msg)
    server.quit()


@receiver(pre_save, sender=Order, dispatch_uid="send mail")
def send_mail_on_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            send_mail(server, instance.customer.email,
                      'Dear Customer,\nYour order status changed from ' + previous.status + ' to ' + instance.status + ' !\n')


class OrderLine(models.Model):
    customized_product = models.ForeignKey(CustomizedProduct, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
