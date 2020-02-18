from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_fsm import FSMField, transition


class BaseModel(models.Model):
    """
    An Abstract model for adding time stamps to all models
    """
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class CustomizableAttribute(BaseModel):
    """
    Some Attributes of a product can be optional like:
    Milk in Latte,
    Shots in Espresso, ...
    We can define this customizable options for each product using this model.
    """
    name = models.CharField(
        "Attribute Name",
        max_length=255,
    )

    def __str__(self):
        return self.name


class CustomizableAttributeOption(BaseModel):
    """
    Each customizable could have some options to be selected by the customer. i.e, Milk for Latte
    can be selected as skim,semi,whole.
    these options can be defined for each product by the manager using this model.
    """
    name = models.CharField(
        "Option Name",
        max_length=255,
    )

    attribute = models.ForeignKey(CustomizableAttribute, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.name


class Product(BaseModel):
    """
    Restbucks Product Model
    """
    product_name = models.CharField(
        "Product Name",
        max_length=255,
    )

    slug = models.SlugField(
        "Slug",
        unique=True,
    )

    unit_price = models.PositiveIntegerField(
        "Unit Price",
    )

    # each product could have some customizable attributes.
    customizable_attributes = models.ManyToManyField(CustomizableAttribute, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        """
        Slugify name of product before save.
        """
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)


class Order(BaseModel):
    """
    This Model is aimed to manage customer Orders contain a state field that manager can change any time.
    """

    customer = models.ForeignKey(
        User,
        verbose_name="Customer",
        related_name='orders',
        on_delete=models.PROTECT,
    )

    state = FSMField(
        default='waiting',
        protected=True,
        verbose_name="Status",
    )

    total_price = models.PositiveIntegerField("Total Price", default=0)

    @transition(field=state, source="waiting", target="preparation")
    def prepare(self):
        # send email to customer
        pass

    @transition(field=state, source="preparation", target="ready")
    def ready(self):
        # send email to customer
        pass

    @transition(field=state, source="ready", target="delivered")
    def deliver(self):
        # send email to customer
        pass

    @transition(field=state, source="waiting", target="canceled")
    def cancel(self):
        # send email to customer
        pass


class OrderItem(BaseModel):
    product = models.ForeignKey(
        Product,
        verbose_name="Product",
        on_delete=models.PROTECT,
    )
    order = models.ForeignKey(
        Order,
        verbose_name="Order",
        related_name='items',
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField("Count", )
    selected_options = models.ManyToManyField(CustomizableAttributeOption, blank=True)
