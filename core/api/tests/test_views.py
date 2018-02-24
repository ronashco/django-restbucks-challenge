from unittest import skip
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from core.orders.models import Cart
from core.accounts.tests import AuthTokenCredentialsMixin
from core.products.models import Product
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


class TestCartListView(APITestCase, AuthTokenCredentialsMixin):
    """
    Make sure core.api.views.CartListView works well.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )

    def setUp(self):
        self.url = reverse('api:cart')

    def test_url(self):
        """Make sure url binds to correct view."""
        self.assertEqual(
            self.client.get(self.url).resolver_match.func.__name__,
            views.CartView.as_view().__name__
        )

    def test_authentication(self):
        """Make sure denies requests with no authentication."""
        response = self.client.post(self.url)  # send request without credentials.‌
        self.assertEqual(
            response.status_code, 401
        )

    def test_response(self):
        self.login(self.user.auth_token.key)
        response = self.client.get(self.url, Authorization="Token %s" % self.user.auth_token.key)
        self.assertEqual(
            response.status_code, 200
        )

        self.assertEqual(
            response['Content-type'], 'application/json'
        )

    def test_database_queries(self):
        """
        Make sure view executes 2 database queries,
        the first one for user authentication and the second one for fetch cart items.
        """
        self.login(self.user.auth_token.key)
        with self.assertNumQueries(2):
            self.client.get(self.url)


class BaseCartTest(APITestCase, AuthTokenCredentialsMixin):
    fixtures = ['products']

    def setUp(self):
        self.url = reverse('api:cart')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )

        cls.product = Product.objects.first()


class CartTest(BaseCartTest):
    """
    Make sure core.api.views.Cart works well.
    """

    def test_url(self):
        self.login(self.user.auth_token.key)
        post_response = self.client.post(self.url)
        self.assertEqual(post_response.resolver_match.func.__name__,
                         views.CartView.as_view().__name__)

        delete_response = self.client.delete(self.url)
        self.assertEqual(delete_response.resolver_match.func.__name__,
                         views.CartView.as_view().__name__)

    def test_authentication_is_required(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

    def test_add_with_invalid_data(self):
        self.login(token=self.user.auth_token.key)

        # request with invalid product data
        response = self.client.post(self.url, data={'product': 1234, 'customization': 'invalid option'})
        self.assertEqual(response.status_code, 400)

        # request with no data
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )

    def test_add_to_cart(self):
        self.login(token=self.user.auth_token.key)

        response = self.client.post(self.url, data={'product': self.product.id,
                                                    'customization': self.product.items[0]})

        self.assertEqual(
            response.status_code, 201
        )
        self.assertEqual(
            1, Cart.objects.count()
        )

    def test_remove_from_cart(self):
        self.login(token=self.user.auth_token.key)

        self.client.post(self.url, data={'product': self.product.id,
                                         'customization': self.product.items[0]})

        response = self.client.delete(self.url, data={'product': self.product.id})
        self.assertEqual(
            response.status_code, 204
        )

        self.assertEqual(0, Cart.objects.count())


class CartViewDatabaseQueriesTest(BaseCartTest):
    """
    Make sure database queries are in the control.
    In every protected url (urls that need user authentication) we need
    a database query to user authentication.
    """
    def test_with_unauthorized_users(self):
        with self.assertNumQueries(0):
            self.client.post(self.url)

    @skip
    def test_with_invalid_product_data(self):
        data = {'product': 123456, 'customization': 'sth'}
        with self.assertNumQueries(2):
            # We need to recognize user and validate product,
            # so it should finish with 2 queries.
            self.login(token=self.user.auth_token.key)

            self.client.post(self.url, data=data)

    @skip
    def test_remove(self):
        data = {'product': self.product.id}
        Cart.objects.create(product=self.product,
                            user=self.user,
                            customization=self.product.items[0])

        with self.assertNumQueries(3):
            # It should done with 3 queries:
            # 1 - user authentication
            # 2 - find
            # 3 - delete cart object
            self.login(token=self.user.auth_token.key)
            self.client.delete(self.url, data=data)

    @skip
    def test_with_valid_product_data(self):
        data = {
            'product': self.product.id,
            'customization': self.product.items[0]
        }
        with self.assertNumQueries(3):
            # It should done with 3 queries:
            # 1 - user authentication
            # 2 - product validation
            # 3 - store cart object
            self.login(token=self.user.auth_token.key)
            self.client.post(self.url, data=data)
