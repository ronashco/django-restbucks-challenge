from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core.products.models import Product

User = get_user_model()


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
                {"customization": "The product (%s) does not support customization"
                                  " however customization field has %s value" %
                                  (self.product, self.customization)}
            )
        elif self.customization is None and self.product.option is not None:
            raise ValidationError(
                {"customization": "Customization can not be null"
                                  "the product (%s) contains option" % self.product}
            )
        elif self.customization is not None and self.customization not in self.product.items:
            raise ValidationError(
                {"customization": "Invalid item %s, choices are %s" %
                                  (self.customization, str(self.product.items))}
            )

    def save(self, **kwargs):
        self.full_clean()
        super(Cart, self).save(**kwargs)


class CartApiModel:
    """
    This class helps cart model serialization
    """
    def __init__(self, count, total_price, products):
        self.count = count
        self.total_price = total_price
        self.products = products
