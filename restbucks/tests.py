from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restbucks.models import Order, OrderProduct
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class AccountTests(APITestCase):
    fixtures = ['product.json']

    def test_create_true_order(self):
        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/'
        data = {
            "items": [
                {"product": 4, "type": None, "count": 1},
                {"product": 1, "type": 1, "count": 1},
                {"product": 2, "type": 4, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_wrong_type_order(self):
        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/'
        data = {
            "items": [
                {"product": 4, "type": 1, "count": 1},
                {"product": 1, "type": 1, "count": 1},
                {"product": 2, "type": 4, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_wrong_type_order2(self):
        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/'
        data = {
            "items": [
                {"product": 4, "type": None, "count": 1},
                {"product": 1, "type": None, "count": 1},
                {"product": 2, "type": 4, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_wrong_type_order3(self):
        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/'
        data = {
            "items": [
                {"product": 4, "type": None, "count": 1},
                {"product": 1, "type": 1, "count": 1},
                {"product": 2, "type": 1, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

    def test_create_wrong_count_order(self):
        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/'
        data = {
            "items": [
                {"product": 4, "type": None, "count": 0},
                {"product": 1, "type": 1, "count": 1},
                {"product": 2, "type": 4, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)

        def test_create_wrong_count_order(self):
            user = User.objects.create(username='test')
            token = Token.objects.create(user=user)

            url = 'http://127.0.0.1:8000/order/'
            data = {
                "items": [
                    {"product": 4, "type": None, "count": -1},
                    {"product": 1, "type": 1, "count": 1},
                    {"product": 2, "type": 4, "count": 2}
                ],
                "consume_location": "sh"
            }
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response = self.client.post(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Order.objects.count(), 0)

    def change_order_status(self):
        self.test_create_true_order()

        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/1/'

        data = {
            "items": [
                {"product": 4, "type": None, "count": 5},

                {"product": 2, "type": 4, "count": 2}
            ],
            "consume_location": "sh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, data, format='json', headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 5)

    def cancel_order_status(self):
        self.test_create_true_order()

        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/1/'

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(url, headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 5)

    def cancel_order_status2(self):
        self.test_create_true_order()
        order = Order.objects.get(pk=1)
        order.status = Order.STATUS_DELIVERED
        order.save()

        user = User.objects.create(username='test')
        token = Token.objects.create(user=user)

        url = 'http://127.0.0.1:8000/order/1/'

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(url, headers={'Authorization': 'Token ' + token.key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 5)