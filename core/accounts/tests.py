from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .backends import EmailBackend

User = get_user_model()


class TestSignals(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User(email='foo@email.com')
        user.set_password('Aab123445678')
        user.save()
        cls.user = user

    def test_token_generated(self):
        """Make sure Token object created"""
        self.assertTrue(
            Token.objects.filter(user=self.user).exists()
        )

    def test_username_sets(self):
        """Make sure username sets automatically as same as email."""
        self.assertEqual(
            self.user.email, self.user.username
        )


class TestEmailBackend(TestCase):
    """
    Make sure backend can recognize users with their email address.
    """
    def setUp(self):
        self.backend = EmailBackend()

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            'email': 'm@email.com',
            'password': 'Abc123456789'
        }
        user = User(email=cls.user_data['email'])
        user.set_password(cls.user_data['password'])
        user.save()
        cls.user = user

    def test_authenticate(self):
        """
        Make sure user returns User object with valid credentials.
        """
        user = self.backend.authenticate(username=self.user_data['email'],
                                         password=self.user_data['password'])
        self.assertEqual(
            self.user, user
        )

    def test_with_invalid_credentials(self):
        """
        Make sure it doesnt accept invalid credentials.
        """
        user = self.backend.authenticate(username=self.user_data['email'],
                                         password='invalid password')
        self.assertIsNone(user)

        user = self.backend.authenticate(username='invalid_username',
                                         password='something ...')
        self.assertIsNone(user)


class AuthTokenCredentialsMixin:
    """
    A Mixin class to handle authentication in protected urls.
    """
    def login(self, token, header_keyword='Token'):
        # set authentication headers to identify user.
        self.client.credentials(HTTP_AUTHORIZATION="%s %s" % (header_keyword, token))
