from rest_framework.test import APILiveServerTestCase
from core.accounts.tests import AuthTokenCredentialsMixin
from .utils import create_user


class BaseCartFunctionalTest(APILiveServerTestCase):
    """
    A helper class to work with cart api.
    """

    fixtures = ['products']

    def setUp(self):
        self.user = create_user()
        self.url = '/api/cart/'

    def add(self, **data):
        return self.client.post(self.url, data=data)

    def remove(self, product_id):
        return self.client.delete(self.url, data={'product': product_id})


class CartOperationsTest(BaseCartFunctionalTest, AuthTokenCredentialsMixin):
    """
    Make sure users can add products to their cart, and also remove from it.
    """

    def test_add(self):
        self.login(token=self.user.auth_token.key)

        response = self.add(product=1, customization='skim')
        self.assertEqual(response.content, b'')

    def test_remove(self):
        self.login(token=self.user.auth_token.key)

        self.add(product=4)

        response = self.remove(4)
        self.assertEqual(
            response.content, b''
        )


class CartListTest(BaseCartFunctionalTest, AuthTokenCredentialsMixin):
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
            self.add(**kwargs)
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
