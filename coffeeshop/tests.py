from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from coffeeshop.models import Product, CustomizableAttribute, CustomizableAttributeOption, Order, OrderItem


class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alireza', password='@12345678')
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {"username": "alireza", "password": "@12345678"}, format='json')
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.latte = Product.objects.create(product_name='Latte', slug='latte', unit_price='2000')
        self.tea = Product.objects.create(product_name='Tea', slug='tea', unit_price='100')
        self.milk = CustomizableAttribute.objects.create(name='Milk')
        self.consume_location = CustomizableAttribute.objects.create(name='Consume location')
        self.skim = CustomizableAttributeOption.objects.create(name='Skim', attribute=self.milk)
        self.semi = CustomizableAttributeOption.objects.create(name='Semi', attribute=self.milk)
        self.whole = CustomizableAttributeOption.objects.create(name='Whole', attribute=self.milk)
        self.take_away = CustomizableAttributeOption.objects.create(name='take away', attribute=self.consume_location)
        self.in_shop = CustomizableAttributeOption.objects.create(name='in shop', attribute=self.consume_location)
        self.latte.customizable_attributes.add(self.milk)
        self.latte.customizable_attributes.add(self.consume_location)
        self.data = {
            "order": [
                {
                    "product": "Latte",
                    "count": 1,
                    "options": [
                        {
                            "name": "Milk",
                            "value": "Semi"
                        },
                        {
                            "name": "Consume location",
                            "value": "take away"
                        }
                    ]
                },
                {
                    "product": "tea",
                    "count": 1,
                    "options": []
                }
            ]
        }

    def test_create_order(self):
        """
        Ensure we can create an order.
        """
        url = reverse('order_create')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_menu(self):
        """
        Ensure we can get the menu.
        """
        url = reverse('product_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_show_orders(self):
        """
        Ensure we can get the user orders.
        """
        self.add_order()
        url = reverse('order_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_cancel_order(self):
        """
        Ensure we can cancel an order.
        """
        order = self.add_order()
        url = reverse('order_cancel')
        response = self.client.post(url, {"order_id": order.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def add_order(self):
        # create new order
        order = Order.objects.create(customer=self.user, total_price=self.latte.unit_price)
        order_item = OrderItem.objects.create(product=self.latte, order=order, count=1)
        order_item.selected_options.add(self.skim)
        order_item.selected_options.add(self.take_away)
        order_item.save()
        return order
