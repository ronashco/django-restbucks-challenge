from django.shortcuts import reverse
from rest_framework.test import APITestCase
from .. import views


class MenuViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:menu')

    def test_url_binds_correct_view(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.resolver_match.func.__name__, views.Menu.as_view().__name__
        )

    def test_response_stuff(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            response['Content-type'], 'application/json'
        )

    def test_executed_queries(self):
        """check database's query count"""
        with self.assertNumQueries(1):
            self.client.get(self.url)
