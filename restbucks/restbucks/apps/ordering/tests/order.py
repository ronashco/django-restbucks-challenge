import json
from random import randint

from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APIClient
from mock import patch

from .base import BaseTestCase


class OrderTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = self.create_user(
            'customer_test',
            'customer@test.com',
            '1qaz2wsx!?'
        )
        response = self.client.post(
            reverse('login'),
            {
                'username': 'customer_test',
                'password': '1qaz2wsx!?'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.customer_token = response.json().get('token')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.customer_token}'
        )
        # Define an admin user
        self.admin = self.create_user(
            'admin_test',
            'admin@test.com',
            '1qaz2wsx!?',
            True,
            True
        )
        response = self.client.post(
            reverse('login'),
            {
                'username': 'admin_test',
                'password': '1qaz2wsx!?'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.admin_token = response.json().get('token')

    def test_register_some_orders_and_retrieve_them(self):
        response = self.client.get(reverse('ordering-menu'))
        menu = response.json()

        length = randint(7, 11)
        for _ in range(length):
            loc = 'in' if randint(0, 9) % 2 else 'out'
            order = {
                'consume_location': loc,
                'delivery_address': 'xyz' if loc == 'out' else '',
                'items': []
            }

            i = randint(0, 5)
            item = {'product_id': menu[i]['id']}
            # product['id'] = menu[i]['id']
            if menu[i]['option_sets']:
                option_set = menu[i]['option_sets'][randint(0, len(menu[i]['option_sets']) - 1)]
                item['option_set_id'] = option_set['id']
                if option_set.get('options', None):
                    item['option_id'] = option_set['options'][
                        randint(0, len(option_set['options']) - 1)
                    ]['id']
            order['items'].append(item)

            response = self.client.post(
                reverse('ordering-orders'),
                json.dumps(order),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 201)

        response = self.client.get(
            reverse('ordering-orders'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), length)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_change_status(self):
        response = self.client.get(reverse('ordering-menu'))
        menu = response.json()

        loc = 'in' if randint(0, 9) % 2 else 'out'
        order = {
            'consume_location': loc,
            'delivery_address': 'xyz' if loc == 'out' else '',
            'items': []
        }

        i = randint(0, 5)
        item = {'product_id': menu[i]['id']}
        # product['id'] = menu[i]['id']
        if menu[i]['option_sets']:
            option_set = menu[i]['option_sets'][randint(0, len(menu[i]['option_sets']) - 1)]
            item['option_set_id'] = option_set['id']
            if option_set.get('options', None):
                item['option_id'] = option_set['options'][
                    randint(0, len(option_set['options']) - 1)
                ]['id']
        order['items'].append(item)

        response = self.client.post(
            reverse('ordering-orders'),
            json.dumps(order),
            content_type='application/json'
        )
        order_info = response.json()
        self.assertEqual(response.status_code, 201)
        response = self.client.put(
            reverse('ordering-delete-or-change', kwargs=dict(pk=order_info['id'])),
            {'status': 'Preparation'},
            content_type='application/json'
        )
        # Owner can't change order status
        self.assertEqual(response.status_code, 403)
        response = self.client.delete(
            reverse('ordering-delete-or-change', kwargs=dict(pk=order_info['id'])),
        )
        self.assertEqual(response.status_code, 403)
        # Admin user can do this successfully
        with patch('restbucks.apps.ordering.tasks.send_mail') as fake_send_mail:
            fake_send_mail = lambda *args, **kwargs: True  # noqa
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
            response = self.client.put(
                reverse('ordering-delete-or-change', kwargs=dict(pk=order_info['id'])),
                json.dumps({'status': 'p'}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 202)

        response = self.client.delete(
            reverse('ordering-delete-or-change', kwargs=dict(pk=order_info['id'])),
        )
        self.assertEqual(response.status_code, 204)
