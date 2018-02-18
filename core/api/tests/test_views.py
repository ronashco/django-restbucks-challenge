from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
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


class LoginTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:login')

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email': 'foo@email.com',
                         'password': 'Abc123456789'}
        cls.user = User.objects.create_user(
            email=cls.user_data['email'],
            username=cls.user_data['email'],
            password=cls.user_data['password']
        )

    def test_response(self):
        """
        Make sure correct STATUS return with either valid or invalid requests.
        """
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )
        # We have no user with bellow credentials.
        response = self.client.post(self.url, data={'email': 'invalid@email.com',
                                                    'password': 'sth'})
        self.assertEqual(
            response.status_code, 400
        )

        self.assertEqual(
            self.client.post(self.url, data=self.user_data).status_code,
            200
        )

    def test_number_of_executed_queries(self):
        """
        Make sure two queries execute with either valid or invalid data.
        The first one is for find user object and the second one is for find token.
        """
        with self.assertNumQueries(2):
            self.client.post(self.url)

        with self.assertNumQueries(2):
            self.client.post(self.url, data={'email': self.user_data['email'],
                                             'password': self.user_data['password']})

        # If the token does not exist, we have to create one, so we one more query.
        Token.objects.filter(user=self.user).delete()
        with self.assertNumQueries(3):
            self.client.post(self.url, data={'email': self.user_data['email'],
                                             'password': self.user_data['password']})
