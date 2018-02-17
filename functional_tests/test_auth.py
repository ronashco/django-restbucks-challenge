from rest_framework.test import APITestCase


class TestRegistration(APITestCase):
    def setUp(self):
        self.url = '/api/accounts/register/'
        self.valid_data = {
            'email': 'foo@email.com',
            'password': 'Abc12345678',
        }

    def test_email_validation(self):
        """
        Users must be enter a valid email address to register.
        """
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.json().get('email'), ['This field is required.']
        )

        data.update({'email': 'invalid_email'})
        response = self.client.post(self.url, data=data)

        self.assertEqual(
            response.json().get('email'), ['Enter a valid email address.']
        )

        data.update({'email': self.valid_data['email']})
        response = self.client.post(self.url, data=data)
        self.assertIsNone(
            response.json().get('email')
        )

    def test_password_validation(self):
        """
         Users must be enter a valid password contains at least 8 letters.
         """
        data = {}
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.json().get('password'), ['This field is required.']
        )

        data.update({'password': '1234567'})
        response = self.client.post(self.url, data=data)

        self.assertEqual(
            response.json().get('password'), ['Password must be contains at least 8 letters.']
        )

        data.update({'password': self.valid_data['password']})
        response = self.client.post(self.url, data=data)
        self.assertIsNone(
            response.json().get('password')
        )

    def test_successful_register(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(
            {'token'}, set(response.json().keys())
        )
