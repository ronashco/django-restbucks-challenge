from django.urls import reverse
from rest_framework.test import APIClient

from .base import BaseTestCase


class MenuTestCase(BaseTestCase):
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

    def test_fetching_menu_list(self):
        response = self.client.get(reverse('ordering-menu'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)
