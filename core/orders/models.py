from django.db import models, connection
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.mail import EmailMessage
from core.products.models import Product

User = get_user_model()
STATUS = {'w': 'Waiting', 'p': 'Preparation',
          'r': 'Ready', 'd': 'Delivered'}
LOCATIONS = {'i': 'In shop', 'a': 'Away'}


class Order(models.Model):
    status = models.CharField(max_length=1, choices=((k, v) for k, v in STATUS.items()),
                              default='w')
    location = models.CharField(max_length=1, choices=((k, v) for k, v in LOCATIONS.items()),
                                default='i')
    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "%s (%s)" % (self.status_label, str(self.date.date()))

    def __str__(self):
        return repr(self)

    @property
    def status_label(self):
        return STATUS.get(self.status, self.status)

    @property
    def location_label(self):
        return LOCATIONS.get(self.location, self.location)

    def _change_status(self, new_status):
        """
        Change object status to :new_status if it exists in :STATUS.
        """
        if new_status in STATUS:
            self.status = new_status
            self.save()

    def prepare(self):
        self._change_status('p')

    def ready(self):
        self._change_status('r')

    def deliver(self):
        self._change_status('d')


class OrderProduct(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    customization = models.CharField(max_length=250, blank=True, null=True)
    price = models.IntegerField()

    def clean(self):
        if self.product.option is None and self.customization is not None:
            """We can customize a product in an order only if it has option value"""

            raise ValidationError("The product does not support customization.")

        elif self.product.option is not None and self.customization is None:
            """If the product has non-null option, the customization is required."""

            raise ValidationError("The product supports customization. The customization is required")
        elif self.customization is not None and self.customization not in self.product.items:
            """Customization must be in product.items"""

            raise ValidationError("customization choices are %s." % ",".join(self.product.items))

    def save(self, **kwargs):
        self.clean()
        super(OrderProduct, self).save(**kwargs)

    class Meta:
        unique_together = ('product', 'order')


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customization = models.CharField(max_length=250, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')

    def clean(self):
        # we will check following conditions,
        # if they are not true we will raise ValidationError:

        # customization must be null if product.option is null
        # customization must be in product.items if product.option is not null

        if self.product.option is None and self.customization is not None:
            raise ValidationError(
                {"customization": "The product does not support customization"}
            )
        elif self.customization is None and self.product.option is not None:
            raise ValidationError(
                {"customization": "The customization can not be null"}
            )
        elif self.customization is not None and self.customization not in self.product.items:
            raise ValidationError(
                {"customization": "Invalid item %s, choices are %s" %
                                  (self.customization, ",".join(self.product.items))}
            )

    def save(self, **kwargs):
        self.full_clean()
        super(Cart, self).save(**kwargs)


class CartApiModel:
    """
    This class helps cart model serialization,
    It has been used only for retrieve data.
    """
    def __init__(self, count, total_price, products):
        self.count = count
        self.total_price = total_price
        self.products = products


class OrderProductApiModel:
    """
    This object helps us to serialize products in orders api.
    Because of some customizations in represent data to clients,
    we will use it in core.api.serializers.OrderSerializer to serialize products.
    e.g. we want to use price field in core.orders.models.OrderProduct.price instead,
    core.orders.models.Order.price.
    """
    def __init__(self, id_, title, price, option, item):
        self.id = id_
        self.title = title
        self.price = price
        self.option = option
        self.item = item


@receiver(post_delete, sender=OrderProduct)
def remove_empty_orders(sender, **kwargs):
    """
    We want to remove Order if it has no related product.
    For less database queries, We execute raw sql.
    """
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM orders_order 
            WHERE id = {order_id} AND (SELECT count(*) FROM orders_orderproduct 
                                       WHERE order_id = {order_id}) = 0;
            """.format(order_id=kwargs['instance'].order_id)
        )


@receiver(post_save, sender=Order)
def change_status(**kwargs):
    """
    We want to notify users after every status modification.
    """
    if not kwargs['created'] and kwargs['instance'].status != 'w':
        message = {
            'w': "Your order is submitted.It's waiting for confirmation",
            'p': "We are preparing your order",
            'r': "Your order is ready.",
            'd': "Your order delivered.",
        }

        try:
            mail = EmailMessage(to=[kwargs['instance'].user.email],
                                body=message[kwargs['instance'].status])
            mail.send()
        except KeyError:
            pass
