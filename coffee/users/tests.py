from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User

class UserAPIViewsTest(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
                email="test@example.com",
                password="test")

    def setUp(self):
        self.super_user = User.objects.create_superuser(email="superuser@example.com",
                                                        password="superuser")


        url = reverse('token_obtain_pair')

        access_token = self.client.post(
                url,
                { "email": self.super_user.email, "password": "superuser" },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


    def test_user_create(self):
        url = reverse('users_list')
        data = {
            "email": "new_user@example.com",
            "password": "new_password"
        }
        response = self.client.post(url, data, format='json') 

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
