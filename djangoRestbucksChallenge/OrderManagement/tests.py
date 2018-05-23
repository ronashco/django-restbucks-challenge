from django.test import TestCase
from OrderManagement.models import Product, CustomizedProduct, Order, OrderLine
from CoffeeShop.models import Customer
from django.urls import reverse
from django.contrib.auth import login


class Test(TestCase):
    def setUp(self):
        c = Customer.objects.create(username="C1", email="C1@C.CCC")
        c.set_password("C1")
        c.save()

        P1 = Product.objects.create(price=1500, name='P1')
        CP11 = CustomizedProduct.objects.create(product=P1, option='size', type='small')
        CP12 = CustomizedProduct.objects.create(product=P1, option='size', type='large')

        P2 = Product.objects.create(price=5000, name='P2')
        CP21 = CustomizedProduct.objects.create(product=P2, option='heat', type='medium')
        CP22 = CustomizedProduct.objects.create(product=P1, option='heat', type='low')

        O1 = Order.objects.create(customer=c, location='coffeeshop')
        OL11 = OrderLine.objects.create(order=O1, customized_product=CP11)

    def test_panel(self):
        self.client.login(username='C1', password='C1')
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'panel.html')

    def test_menu(self):
        self.client.login(username='C1', password='C1')
        response = self.client.get(reverse('menu'))
        all_products = Product.objects.all()
        for product in response.context[-1]['products']:
            self.assertTrue(product in all_products)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')

    #TODO
    def new_order(self):
        P1 = Product.objects.get(pk=1)
        cp = P1.customizedproduct_set.first()
        data = {str(P1.pk): [cp.option + '-' + cp.type], 'location': ['takeaway']}

    def test_view_orders(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_orders.html')