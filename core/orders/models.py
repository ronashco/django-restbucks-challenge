from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    order = models.ForeignKey(Order, related_query_name='products', related_name='products')
    customization = models.CharField(max_length=250, blank=True, null=True)
    unit_price = models.IntegerField()
    count = models.IntegerField(default=1)

    def clean(self):
        if self.product.option is None and self.customization is not None:
            """We can customize a product in an order only if it has option value"""

            raise ValidationError("The product (%s) doesnt support customization." % self.product)

        elif self.product.option is not None and self.customization is None:
            """If the product has non-null option, the customization is required."""

            raise ValidationError("The product (%s) does not support customization." % self.product)
        elif self.customization not in self.product.items:
            """Customization must be in product.items"""

            raise ValidationError("customization choices are %s." % ",".join(self.product.items))

    def save(self, **kwargs):
        self.clean()
        super(OrderProduct, self).save(**kwargs)

    class Meta:
        unique_together = ('product', 'order')
