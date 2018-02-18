from rest_framework.test import APILiveServerTestCase, APIClient
client = APIClient()


# a helper that adds product to cart.
def add(**data):
    return client.post('/api/cart/', data=data)


# a helper that removes product from cart.
def remove(product_id):
    return client.delete('/api/cart/', data={'product': product_id})


class CartOperationsTest(APILiveServerTestCase):
    """
    Make sure users can add products to their cart, and also remove from it.
    """

    fixtures = ['products']

    def test_add(self):
        response = add(product_id=1, option='skim')
        self.assertEqual(response.json(), {'message': 'Product added to cart.',
                                           'cart_count': 1})

    def test_remove(self):
        response = add(product_id=1, option='semi')
        self.assertEqual(
            response.json(), {'message': 'Product removed.', 'cart_count': 0}
        )


class CartListTest(APILiveServerTestCase):
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
    fixtures = ['products']

    def setUp(self):
        self.url = '/api/cart/'

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
            kwargs = {'product_id': product['id']}
            product_dict = {'title': product['title'], 'price': product['price']}
            if product['option'] is not None:
                # select a random option
                item = random.choice(product['items'])
                kwargs.update({'option': item})
                product_dict.update({'option': product['option'], 'selected_item': item})
            add(**kwargs)
            total_price += product['price']
            result.append(product_dict)

        return total_price, count, result

    def test_list(self):
        total_price, count, products = self._prepare_data()

        response = self.client.get(self.url)

        self.assertEqual(response.json(), {'count': count,
                                           'total_price': total_price,
                                           'products': products})
