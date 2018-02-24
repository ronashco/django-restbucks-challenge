class OrderSTest(BaseOrderFunctionalTest, AuthTokenCredentialsMixin):
    def test_submit_order(self):
        """
        Make sure users can submit order.
        """
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=1, customization='skim')
        self.add_to_card(product=2, customization='small')

        response = self.client.post('/api/orders/')
        result = {
            'url': response.wsgi_request.build_absolute_uri('/api/orders/1'),
            'total_price': 11,
            'status': 'Waiting',
            'location': 'In Shop',
            'date': str(datetime.now().date()),
            'products': [
                {'title': 'Latte', 'price': 5, 'customization': 'skim'},
                {'title': 'Cappuccino', 'price': 6, 'customization': 'small'}
            ]
        }
        json = response.json()
        for p in result['products']:
            self.assertIn(p, json['products'])

        result.pop('products')
        json.pop('products')

        self.assertEqual(json, result)

    def test_cancel_a_waiting_order(self):
        """
        Make sure users can cancel an order.
        """
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=1, customization='skim')

        self.client.post('/api/orders/')  # submit order.

        response = self.client.delete('/api/orders/1')

        self.assertEqual(
            response.content, b''
        )

        # make sure we have no order
        self.assertEqual(
            self.client.get('/api/orders/').json(),
            dict()
        )

    def test_can_change_a_waiting_order(self):
        self.login(token=self.user.auth_token.key)

        self.add_to_card(product=1, customization='skim')
        self.client.post('/api/orders/')  # submit order.

        self.client.patch('/api/orders/1/product/1/',
                          data={'customization': 'semi'})

        orders = self.client.get('/api/orders/')
        self.assertEqual(orders.json()[0], {
            ''
        })

# PATCH /orders/1/product/2 =>‌ change customization
# DELETE /orders/1/product/2 => remove product from order
