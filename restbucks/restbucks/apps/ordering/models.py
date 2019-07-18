from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


UserModel = get_user_model()


class BaseModel(models.Model):
    """
    Some Properties and Methods That Is Common
    Between All Models Implemented In This Abstract Model
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    soft_deleted = models.BooleanField(default=False, editable=False)

    def delete(self, deep_remove=False, *args, **kwargs):
        if deep_remove is False:
            self.soft_deleted = True
            self.save()
            return
        super(BaseModel, self).delete(*args, **kwargs)


class OptionSet(BaseModel):
    """
    A Bundle Of Choices To Determining Special Value
    For Certain Aspect Of Product When Client Registering An Order
    """
    class Meta:
        verbose_name = _('Option Set')
        verbose_name_plural = _('Option Sets')
        unique_together = [('name', 'product')]

    name = models.CharField(max_length=100)
    product = models.ForeignKey(
        'Product',
        related_name='option_sets',
        on_delete=models.CASCADE
    )


class Option(BaseModel):
    """
    Item Of Option-Set
    """
    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')
        unique_together = [
            ('option_set', 'value')
        ]

    value = models.SlugField(max_length=50)
    option_set = models.ForeignKey(
        OptionSet,
        related_name='options',
        on_delete=models.CASCADE
    )


class Product(BaseModel):
    """
    All Products Saving To Db By Using This Model
    (Default Products Initiated In 0002_auto_... Migration File)
    """
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=80)
    price = models.IntegerField(
        default=10_000, help_text=_('Enter price value in Toman currency')
    )


class OrderItem(BaseModel):
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.DO_NOTHING)
    option_set = models.ForeignKey(OptionSet, on_delete=models.DO_NOTHING, null=True)
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING, null=True)


class Order(BaseModel):
    """
    Entity For Save Clients Orders
    """
    CONSUME_LOCATION_CHOICES = [
        ('in', _('In Shop')),
        ('out', _('Take Away'))
    ]

    STATUS_CHOICES = [
        ('w', 'Waiting'),
        ('p', 'Preparation'),
        ('r', 'Ready'),
        ('d', 'Delivered')
    ]

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    client = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders', through=OrderItem)
    total_price = models.BigIntegerField(blank=True, null=True, editable=False)
    consume_location = models.CharField(choices=CONSUME_LOCATION_CHOICES, max_length=3)
    delivery_address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        if self.total_price is None:
            self.total_price = self.items.aggregate(
                models.Sum('product__price')
            )['product__price__sum']
        return super(Order, self).save(*args, **kwargs)
