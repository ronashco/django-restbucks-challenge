from django.test import TestCase
from OrderManagement.models import Product, CustomizedProduct, Order, OrderLine
from CoffeeShop.models import Customer
from django.urls import reverse
from django.contrib.auth import login
from django.test import Client
from django.db.models import Sum


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
        self.assertQuerysetEqual(response.context[-1]['products'], [p.__repr__() for p in all_products], ordered=False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')

    def test_new_order(self):
        user = self.client.login(username='C1', password='C1')
        c = Client()
        P1 = Product.objects.get(pk=1)
        cp = P1.customizedproduct_set.first()
        data = {str(P1.pk): [cp.option + '-' + cp.type], 'location': ['takeaway']}
        print(Order.objects.filter(customer=user).last().pk)
        c.post('/customer/order', data)
        print(Order.objects.filter(customer=user).last().pk)
        print('*****************')
        self.assertTrue(True)

    def test_view_orders(self):
        user = self.client.login(username='C1', password='C1')
        response = self.client.get(reverse('orders'))
        self.assertQuerysetEqual(response.context[-1]['orders'], [o.__repr__() for o in Order.objects.filter(customer=user)], ordered=False)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_orders.html')

    def test_view_an_order(self):
        user = self.client.login(username='C1', password='C1')
        order = Order.objects.filter(customer=user).first()
        response = self.client.get(reverse('view_an_order')+'?id='+str(order.pk)).context[-1]

        price = OrderLine.objects.filter(order=order).aggregate(Sum('customized_product__product__price'))
        price = price['customized_product__product__price__sum']
        self.assertEqual(response['price'], price)

        self.assertEqual(response['order'], order)

        result = [cp[0] for cp in order.orderline_set.values_list('customized_product_id')]
        self.assertEqual(result, response['my_customized_products_id'])

