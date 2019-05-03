from django.db import models
from django.contrib.auth.models import User


class ProductType(models.Model):
    name = models.CharField('Name', max_length=200, null=False, blank=False, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('Name', max_length=200, null=False, blank=False, unique=True)
    image = models.URLField('Image URL', null=True, blank=True)
    price = models.PositiveIntegerField('Price')
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(ProductType, on_delete=models.PROTECT, db_index=True, null=True, blank=True)

    def __str__(self):
        return "%s:%s" % (self.name, self.price)


class ProductOrderType(models.Model):
    name = models.CharField('Name', max_length=200, null=False, blank=False)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s:%s" % (self.product_type, self.name)


class Order(models.Model):
    STATUS_WAITING = 'wa'
    STATUS_PREPARATION = 'pr'
    STATUS_READY = 'rd'
    STATUS_DELIVERED = 'de'
    STATUS_UNKNOWN = 'uk'
    STATUS_CANCEL = 'ca'
    STATUS_CHOICE = (
        (STATUS_WAITING, 'waiting'),
        (STATUS_PREPARATION, 'preparation'),
        (STATUS_READY, 'ready'),
        (STATUS_DELIVERED, 'delivered'),
        (STATUS_CANCEL, 'cancel'),
        (STATUS_UNKNOWN, 'unknown'),
    )

    CONSUME_LOCATION_IN_SHOP = 'sh'
    CONSUME_LOCATION_TAKEAWAY = 'ta'
    CONSUME_LOCATION_CHOICE = (
        (CONSUME_LOCATION_IN_SHOP, 'in shop'),
        (CONSUME_LOCATION_TAKEAWAY, 'takeaway')
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICE,default=STATUS_WAITING)
    consume_location = models.CharField(max_length=2, choices=CONSUME_LOCATION_CHOICE)
    total_price = models.PositiveIntegerField('Total Price')
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT, db_index=True)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, db_index=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, db_index=True)
    product_order_type = models.ForeignKey(ProductOrderType, on_delete=models.PROTECT, db_index=True, null=True, blank=True)
    price = models.PositiveIntegerField('Price', default=0)  # if change product price do not change older order item price
    count = models.PositiveSmallIntegerField('Count', default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "%s:%s:%s" % (self.product, self.product_order_type, self.order)
