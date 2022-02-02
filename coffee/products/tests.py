from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from products.models import Product, AvailableProductOption

class ProductAPIViewsTest(APITestCase):
    
    """ Setup test data """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
                email="test@example.com",
                password="test")

    def setUp(self):
        self.super_user = User.objects.create_superuser(email="superuser@example.com",
                                                        password="superuser")
        self.product = Product.objects.create(name="Cappuccino") 
        self.available_product = AvailableProductOption.objects.create(option="Small",
                                                             product=self.product) 

        url = reverse('token_obtain_pair')

        access_token = self.client.post(
                url,
                { "email": self.super_user.email, "password": "superuser" },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


    def test_product_receive(self):
        url = reverse('product_actions-list')
 
        response = self.client.get(url, format='json') 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
