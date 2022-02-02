from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from orders.models import OrderItem, Order
from products.models import Product, AvailableProductOption

class OrderAPIViewsTest(APITestCase):
    
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
        self.order = Order.objects.create()

        url = reverse('token_obtain_pair')

        access_token = self.client.post(
                url,
                { "email": self.super_user.email, "password": "superuser" },
                format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


    def test_order_creation(self):
        url = reverse('order_actions-list')

        data = {
            "order_items": [
                {
                    "product_id": self.product.id,
                    "option": "Small"
                }
            ]
        }
        response = self.client.post(url, data, format='json') 

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_receive(self):
        url = reverse('order_actions-list')
 
        response = self.client.get(url, format='json') 

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_cancel(self):

        url = reverse('order_actions-detail', args=[self.order.id])

        response = self.client.delete(url, format='json')
  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Order canceled")

    def test_order_update(self):

        url = reverse('order_actions-detail', args=[self.order.id])
        data = {
            "status": "Preparation"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
