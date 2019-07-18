from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from ..models import Order, OrderItem
from ..tasks import send_status_email


class OrderService(object):
    @staticmethod
    def create_order_on_the_fly():
        return Order()

    @staticmethod
    def create_order(products, consume_location, delivery_address):
        order = Order(
            consume_location=consume_location,
            delivery_address=delivery_address,
        )

        for product in products:
            order.products.add(product)

        return order

    @staticmethod
    def get(**filters):
        return Order.objects.get(soft_deleted=False, **filters)

    @staticmethod
    def all_orders_of(client):
        return Order.objects.filter(
            soft_deleted=False,
            client=client
        )

    @staticmethod
    def add_item(order, product, option_set, option):
        return OrderItem.objects.create(
            order=order, product=product, option_set=option_set, option=option
        )

    @staticmethod
    def update_status(order_id, status):
        with transaction.atomic():
            # Lock order for changing status by using the "select_for_update"
            order = Order.objects.select_for_update().get(id=order_id)
            order.status = status
            order.save()
            send_status_email.delay(
                order.client.email, dict(Order.STATUS_CHOICES).get(status)
            )
        return order

    @staticmethod
    def delete(order):
        order.delete()
        send_status_email.delay(
            order.client.email, _('Canceled')
        )
