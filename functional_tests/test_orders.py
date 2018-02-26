from datetime import datetime
from django.test import tag
from rest_framework.test import APILiveServerTestCase
from core.accounts.tests import AuthTokenCredentialsMixin
from .utils import create_user


class BaseOrderFunctionalTest(APILiveServerTestCase):
    """
    A helper class to work with cart api.
    """

    fixtures = ['products']

    def setUp(self):
        self.user = create_user()
        self.url = '/api/orders/cart/'

    def add_to_card(self, **data):
        return self.client.post(self.url, data=data)

    def remove_from_cart(self, product_id):
        return self.client.delete(self.url, data={'product': product_id})


class CartOperationsTest(BaseOrderFunctionalTest, AuthTokenCredentialsMixin):
    """
    Make sure users can add products to their cart, and also remove from it.
    """

    def test_add(self):
        self.login(token=self.user.auth_token.key)

        response = self.add_to_card(product=1, customization='skim')
        self.assertEqual(response.content, b'')

    def test_remove(self):
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=4)

        response = self.remove_from_cart(4)
        self.assertEqual(
            response.content, b''
        )


class CartListTest(BaseOrderFunctionalTest, AuthTokenCredentialsMixin):
    """
    Make sure users are able to view their cart list.
    the result must be something like the following object:
    {
        "count":‌ X,
        "total_price":‌ X,
        "products: [
            {
                "title":‌ "product_1",
                "price":‌ "a",
                "option": "an_option",
                "selected_item": "an_item"
            },
            {
                "title":‌ "product_2",
                "price":‌ "a2",
                "option": "an_option",
                "selected_item": "an_item"
            },
            ...
        ]

    }
    """

    def _prepare_data(self):
        import random
        count = 3
        # following code gets products using api.
        products = self.client.get('/api/products/').json()
        total_price = 0
        # The result variable should be same as a list of products in cart list response.
        result = []
        for i in range(count):
            product = products[i]
            kwargs = {'product': product['id']}
            product_dict = {'title': product['title'], 'price': product['price'],
                            'id': product['id']}
            if product['option'] is not None:
                # select a random option
                item = random.choice(product['items'])
                kwargs.update({'customization': item})
                product_dict.update({'option': product['option'], 'selected_item': item})
            self.add_to_card(**kwargs)
            total_price += product['price']
            result.append(product_dict)

        return total_price, count, result

    def test_list(self):
        self.login(token=self.user.auth_token.key)

        total_price, count, products = self._prepare_data()

        json = self.client.get(self.url).json()

        self.assertEqual(
            int(json.get('total_price')), total_price
        )
        self.assertEqual(
            int(json.get('count')), count
        )

        for p in products:
            self.assertIn(
                p, json['products']
            )


class OrderListTest(BaseOrderFunctionalTest, AuthTokenCredentialsMixin):
    def test_fetch_orders_list(self):
        """
        Users must get a list of products in /api/orders/ url.
        The response is something like:
        [
            {
                id:‌‌ X1,
                total_price: X,
                status: X,
                url: our_domain/api/orders/X1,
            },
            {
                id:‌‌ X2,
                total_price: X,
                status: X,
                url: our_domain/api/orders/X2,
            },
            ...
        ]
        """
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=1, customization='skim')
        self.add_to_card(product=2, customization='medium')

        self.client.post('/api/orders/')  # submit orders.

        response = self.client.get('/api/orders/')
        json = response.json()[0]

        self.assertIn('id', json.keys())
        self.assertEqual(json['total_price'], 11)
        self.assertEqual(json['status'], 'Waiting')
        # TODO:‌ add url to serializer.
        # self.assertEqual(
        #     json['url'], response.wsgi_request.build_absolute_uri('/api/orders/1/')
        # )

    @tag('future')
    def test_fetch_order_item(self):
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=1, customization='skim')
        self.add_to_card(product=2, customization='medium')

        self.client.post('/api/orders/', data={'location': 'a'})

        json = self.client.get('/api/orders/1/').json()

        self.assertEquals(
            json['total_price'], 11
        )
        self.assertEquals(
            json['status'], 'w'
        )

        self.assertEquals(
            json['location'], 'a'
        )

        date = datetime.now().strftime("%d %b %Y-%H:%M")

        self.assertEquals(
            json['date'], date
        )

        products = [
            {'title': 'Latte', 'price': 5, 'option': 'Milk', 'item': 'skim', 'id': 1},
            {'title': 'Cappuccino', 'price': 6, 'option': 'Size', 'item': 'medium', 'id': 2},
        ]

        for p in products:
            self.assertIn(
                p, json['products']
            )
