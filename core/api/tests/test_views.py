from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .. import views

User = get_user_model()


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


class RegistrationTest(APITestCase):
    """
    Make sure register view works.
    """
    def setUp(self):
        self.url = reverse('api:register')
        self.user_data = {
            'email': 'foo@email.com',
            'password': 'Abc1234566778'}

    def test_url_binds_correct_view(self):
        response = self.client.post(self.url)
        self.assertEqual(
            response.resolver_match.func, views.register
        )

    def test_denies_invalid_credentials(self):
        """
        Check HTTP‌ STATUS for invalid requests.
        """
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )

    def test_user_created(self):
        """
        Check database to measurement data stored.
        """
        self.client.post(self.url, data=self.user_data)
        self.assertTrue(
            User.objects.filter(email=self.user_data['email']).exists()
        )

    def test_successful_response(self):
        """
        Make sure correct token returns.
        """
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(
            response.status_code, 201
        )
        self.assertEqual(
            response.json(), {'token': User.objects.get(email=self.user_data['email']).auth_token.key}
        )
