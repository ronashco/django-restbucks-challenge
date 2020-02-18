from __future__ import absolute_import, unicode_literals
import time

from celery import shared_task
from django.contrib.auth.models import User

from coffeeshop.models import Order, Product, OrderItem
from restbucks.celery_app import app as celery_app


@shared_task
def do_some_queries():
    pass


@shared_task
def create_order(user_id, items):
    order = Order.objects.create(customer_id=user_id)
    for item in items:
        selected_product = Product.objects.filter(product_name__iexact=item.get('product')).first()
        if not selected_product:
            continue
        order_item = OrderItem.objects.create(product=selected_product, order=order, count=item.get('count'))
        order.total_price += selected_product.unit_price
        for option in item.get('options'):
            selected_product_attr = selected_product.customizable_attributes.filter(name__iexact=option.get('name')).first()
            if selected_product_attr:
                selected_option = selected_product_attr.options.filter(name__iexact=option.get('value')).first()
                if selected_option:
                    order_item.selected_options.add(selected_option)
                    order_item.save()
    order.save()
