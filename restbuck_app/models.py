from django.db import models
from django.contrib.auth.models import User


class ConsumeLocation(models.Model):
    take_away = 0
    in_shop = 1
    types = (
        (take_away, 'take away'),
        (in_shop, 'in shop'),
    )


class OrderStatus(models.Model):
    waiting = 0
    preparation = 1
    ready = 2
    delivered = 3
    canceled = 4
    types = (
        (waiting, 'waiting'),
        (preparation, 'preparation'),
        (ready, 'ready'),
        (delivered, 'delivered'),
        (canceled, 'canceled'),
    )


class Feature(models.Model):
    title = models.CharField(max_length=255)
    # TODO: change to 'label' and 'code' to support multiple 'kind' for different product

    def __str__(self):
        return self.title

    def get_values(self):
        return ', '.join([y.title for y in FeaturesValue.objects.filter(feature=self)])


class FeaturesValue(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.feature.title+'-->'+self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    cost = models.IntegerField()
    feature_list = models.ManyToManyField(Feature, through='ProductFeature')

    def __str__(self):
        return self.title

    @property
    def feature_lists(self):
        return ', '.join([x.title for x in self.feature_list.all()])

    @property
    def feature_list_with_values(self):
        return ', '.join([x.title+': '+x.get_values() for x in self.feature_list.all()])


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title+' '+self.feature.title


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    count = models.IntegerField()
    consume_location = models.SmallIntegerField(choices=ConsumeLocation.types)
    feature_value = models.ForeignKey(FeaturesValue, on_delete=models.PROTECT)

    def __str__(self):
        return self.count.__str__()+'*'+self.product.title+'--orderNo: '+self.order.id.__str__()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.SmallIntegerField(choices=OrderStatus.types, default=OrderStatus.waiting)
    product_list = models.ManyToManyField(Product, through=ProductOrder, related_name='products')

    def __str__(self):
        return 'id:'+self.id.__str__() + '-' + self.user.__str__() + '-' + ', '.join([x.title for x in self.product_list.all()])

