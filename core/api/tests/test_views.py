from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.test import tag
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from core.orders.models import Cart, Order, OrderProduct
from core.accounts.tests import AuthTokenCredentialsMixin
from core.products.models import Product
from django.core import mail
from .. import views


User = get_user_model()


class MenuViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:menu')

    def test_url_binds_correct_view(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.resolver_match.func.__name__, views.Menu.as_view().__name__
        )

    def test_response_stuff(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            response['Content-type'], 'application/json'
        )

    def test_executed_queries(self):
        """check database's query count"""
        with self.assertNumQueries(1):
            self.client.get(self.url)


class RegistrationTest(APITestCase):
    """
    Make sure register view works.
    """
    def setUp(self):
        self.url = reverse('api:register')
        self.user_data = {
            'email': 'foo@email.com',
            'password': 'Abc1234566778'}

    def test_url_binds_correct_view(self):
        response = self.client.post(self.url)
        self.assertEqual(
            response.resolver_match.func, views.register
        )

    def test_denies_invalid_credentials(self):
        """
        Check HTTP‌ STATUS for invalid requests.
        """
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )

    def test_user_created(self):
        """
        Check database to measurement data stored.
        """
        self.client.post(self.url, data=self.user_data)
        self.assertTrue(
            User.objects.filter(email=self.user_data['email']).exists()
        )

    def test_successful_response(self):
        """
        Make sure correct token returns.
        """
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(
            response.status_code, 201
        )
        self.assertEqual(
            response.json(), {'token': User.objects.get(email=self.user_data['email']).auth_token.key}
        )


class LoginTest(APITestCase):
    def setUp(self):
        self.url = reverse('api:login')

    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email': 'foo@email.com',
                         'password': 'Abc123456789'}
        cls.user = User.objects.create_user(
            email=cls.user_data['email'],
            username=cls.user_data['email'],
            password=cls.user_data['password']
        )

    def test_response(self):
        """
        Make sure correct STATUS return with either valid or invalid requests.
        """
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )
        # We have no user with bellow credentials.
        response = self.client.post(self.url, data={'email': 'invalid@email.com',
                                                    'password': 'sth'})
        self.assertEqual(
            response.status_code, 400
        )

        self.assertEqual(
            self.client.post(self.url, data=self.user_data).status_code,
            200
        )

    def test_number_of_executed_queries(self):
        """
        Make sure two queries execute with either valid or invalid data.
        The first one is for find user object and the second one is for find token.
        """
        with self.assertNumQueries(2):
            self.client.post(self.url)

        with self.assertNumQueries(2):
            self.client.post(self.url, data={'email': self.user_data['email'],
                                             'password': self.user_data['password']})

        # If the token does not exist, we have to create one, so we one more query.
        Token.objects.filter(user=self.user).delete()
        with self.assertNumQueries(3):
            self.client.post(self.url, data={'email': self.user_data['email'],
                                             'password': self.user_data['password']})


class BaseCartViewTest(APITestCase, AuthTokenCredentialsMixin):
    """
    Make sure core.api.views.CartListView works well.
    """
    url = reverse('api:cart')
    fixtures = ['products']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )
        cls.product = Product.objects.first()

    def test_url(self):
        """Make sure url binds to correct view."""
        self.assertEqual(
            self.client.get(self.url).resolver_match.func.__name__,
            views.CartView.as_view().__name__
        )

    def test_authentication(self):
        """Make sure denies requests with no authentication."""
        response = self.client.post(self.url)  # send request without credentials.‌
        self.assertEqual(
            response.status_code, 401
        )

    def test_response(self):
        self.login(self.user.auth_token.key)
        response = self.client.get(self.url, Authorization="Token %s" % self.user.auth_token.key)
        self.assertEqual(
            response.status_code, 200
        )

        self.assertEqual(
            response['Content-type'], 'application/json'
        )

    def test_db_queries_with_unauthorized_users(self):
        with self.assertNumQueries(0):
            self.client.post(self.url)


class CreateCartTest(BaseCartViewTest):
    """
    Test core.api.CartView with POST requests.
    """

    def test_add_with_invalid_data(self):
        """
         Make sure view prevents invalid requests.
        """
        self.login(token=self.user.auth_token.key)

        # request with invalid product data
        data = {'product': 1234, 'customization': 'invalid option'}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)

        # request with no data
        self.assertEqual(
            self.client.post(self.url).status_code, 400
        )

        self.assertEqual(0, Cart.objects.count())

    def test_add_to_cart(self):
        self.login(token=self.user.auth_token.key)

        response = self.client.post(self.url, data={'product': self.product.id,
                                                    'customization': self.product.items[0]})

        self.assertEqual(
            response.status_code, 201
        )
        self.assertEqual(
            1, Cart.objects.count()
        )

    def test_db_with_invalid_product_data(self):
        data = {'product': 123456, 'customization': 'sth'}
        with self.assertNumQueries(2):
            # We need to recognize user and validate product,
            # so it should finish with 2 queries.
            self.login(token=self.user.auth_token.key)

            self.client.post(self.url, data=data)

    @tag('unresolved')
    def test_with_valid_product_data(self):
        data = {
            'product': self.product.id,
            'customization': self.product.items[0]
        }
        with self.assertNumQueries(3):
            # It should done with 3 queries:
            # 1 - user authentication
            # 2 - product validation
            # 3 - store cart object
            self.login(token=self.user.auth_token.key)
            self.client.post(self.url, data=data)


class ModifyCartTest(BaseCartViewTest):
    """
    Test core.api.CartView with PATCH/DELETE requests.
    """
    def test_remove_from_cart(self):
        self.login(token=self.user.auth_token.key)

        self.client.post(self.url, data={'product': self.product.id,
                                         'customization': self.product.items[0]})

        response = self.client.delete(self.url, data={'product': self.product.id})
        self.assertEqual(
            response.status_code, 204
        )

        self.assertEqual(0, Cart.objects.count())

    def test_deletion_db_queries(self):
        data = {'product': self.product.id}
        Cart.objects.create(product=self.product,
                            user=self.user,
                            customization=self.product.items[0])

        with self.assertNumQueries(3):
            # It should done with 3 queries:
            # 1 - user authentication
            # 2 - find
            # 3 - delete cart object
            self.login(token=self.user.auth_token.key)
            self.client.delete(self.url, data=data)


class BaseOrderListCreateViewTest(APITestCase, AuthTokenCredentialsMixin):
    fixtures = ['products']
    url = reverse('api:orders')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='foo@email.com',
            username='foo@email.com',
            password='Abc123456789',
        )

    def test_authentication(self):
        """Make sure authentication is required."""
        self.assertEqual(
            401, self.client.get(self.url).status_code
        )
        self.login(token=self.user.auth_token.key)  # send login auth credentials.
        self.assertEqual(
            self.client.get(self.url).status_code, 200
        )

    def test_url(self):
        """
        Make sure url connected to related view.
        """
        response = self.client.get(self.url)
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.OrderListCreateView.as_view().__name__
        )


class OrderListViewTest(BaseOrderListCreateViewTest):
    """
    Test core.orders.views.OrderListCreateView with GET requests.
    """
    def test_executed_queries(self):
        with self.assertNumQueries(2):
            self.login(token=self.user.auth_token.key)
            self.client.get(self.url)


class OrderCreateViewTest(BaseOrderListCreateViewTest):
    """
    Test core.api.OrderListCreateView with POST requests.
    """
    def test_validation(self):
        self.login(token=self.user.auth_token.key)

        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

    def test_submit_order(self):
        self.login(token=self.user.auth_token.key)
        self.client.post(reverse('api:cart'), {'product': 1, 'customization': 'skim'})
        self.client.post(reverse('api:cart'), {'product': 4})

        self.client.post(self.url)

        self.assertEqual(
            1, Order.objects.count()
        )

        self.assertEqual(
            0, Cart.objects.count()
        )

        self.assertEqual(
            OrderProduct.objects.count(), 2
        )

    def test_stored_order(self):
        self.login(token=self.user.auth_token.key)
        self.client.post(reverse('api:cart'), {'product': 1, 'customization': 'skim'})
        self.client.post(reverse('api:cart'), {'product': 4})

        self.client.post(self.url, {'location': 'a'})

        order = Order.objects.first()

        self.assertEqual(
            self.user, order.user
        )

        self.assertEqual(
            order.total_price, 7
        )

        self.assertEqual(
            order.location, 'a'
        )

    def test_executed_queries(self):
        self.login(token=self.user.auth_token.key)
        r1 = self.client.post(reverse('api:cart'), data={'product': 4})
        r2 = self.client.post(reverse('api:cart'), data={'product': 1,
                                                         'customization': 'skim'})
        if r1.status_code != 201 or r2.status_code != 201:
            self.fail()

        """
        In Create view we need 6 database queries:
        - check user authentication.
        - check cart validation (cart must be contains at least 1 item).
        - create order.
        - fetch cart items. 
        - delete cart items.
        - create OrderProduct objects.
        - update order's total price
        """
        with self.assertNumQueries(7):
            self.client.post(self.url)


class BaseOrderViewTest(APITestCase, AuthTokenCredentialsMixin):

    fixtures = ['products']
    url_namespace = 'api:order'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='foo@email.com',
            username='foo@email.com',
            password='Abc123456789',
        )
        cls.order = Order.objects.create(
            user=cls.user,
            total_price=0
        )

    def url(self, *args):
        return reverse(self.url_namespace, args=args)

    def test_authentication(self):
        """
        Make sure access needs authentication.
        :return:
        """
        response = self.client.get(reverse(self.url_namespace, args=(self.order.id,)))
        self.assertEqual(
            401, response.status_code
        )

    def test_bound_view(self):
        self.login(token=self.user.auth_token.key)
        response = self.client.get(self.url(self.order.id))
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.OrderView.as_view().__name__
        )

    def rest_url(self):
        """
        Make sure url regular expression wrote properly.
        """
        self.login(token=self.user.auth_token.key)
        response = self.client.get(self.url(self.order.id))
        self.assertEqual(
            response.status_code, 200
        )

        response = self.client.get(self.url('a' + str(self.order.id)))
        self.assertEqual(response.status_code, 404)


class RetrieveDetailOrderTest(BaseOrderViewTest):

    def test_user_has_access_his_orders_only(self):
        """
        Make sure users cannot access to other people data
        through enter order id in url.
        """
        user = User.objects.create_user(email='new_user@email.com',
                                        username='new_user@email.com',
                                        password='abc123456789')

        self.login(token=user.auth_token.key)
        response = self.client.get(self.url(self.order.id))
        self.assertEqual(
            response.status_code, 404
        )


class RetrieveDetailOrderDatabaseQueriesTest(BaseOrderViewTest):
    """
    Test number of database queries in difference situations
    for fetch an order object and related products.
    """
    def test_with_anonymous_user(self):
        """
        Check database queries for users with no auth credentials.
        """
        with self.assertNumQueries(0):
            self.client.get(self.url(1))

    def test_with_unrelated_user(self):
        """
        Check database queries for a user who requested another user data.
        """
        user = User.objects.create_user(email='new_user@email.com',
                                        username='new_user@email.com',
                                        password='abc123456789')
        self.login(token=user.auth_token.key)
        with self.assertNumQueries(2):
            """
            It should be done with 2 queries,
            The first one for user authentication and the second one for find order.
            """
            self.client.get(self.url(2))

    def test_retrieve(self):
        """
        Check database queries for fetch order and related products.
        """
        self.login(self.user.auth_token.key)
        order = Order.objects.create(
            user=self.user,
            total_price=0
        )
        # Prepare data.
        p1 = Product.objects.first()
        p2 = Product.objects.get(title='Tea')
        p3 = Product.objects.get(title='Cookie')
        OrderProduct.objects.create(
            product=p1,
            order=order,
            customization=p1.items[0],
            price=p1.price
        )
        OrderProduct.objects.create(
            product=p2,
            order=order,
            price=p2.price
        )

        OrderProduct.objects.create(
            product=p3,
            order=order,
            customization=p3.items[0],
            price=p2.price
        )

        with self.assertNumQueries(4):
            """
            It should be done with 4 database queries.
            The first one for check authentication,
            and the next three ones for fetch order and related products.
            """
            self.client.get(self.url(order.id))


class OrderUpdateViewTest(BaseOrderViewTest):
    """
    Test OrderView with put/patch.
    """

    def test_users_can_update_only_their_orders(self):
        """
        Make sure users cant update other people.
        """
        user = User.objects.create_user(email='new_user@email.com',
                                        username='new_user@email.com',
                                        password='abc123456789')
        self.login(token=user.auth_token.key)
        response = self.client.patch(self.login(self.order.id))
        self.assertEqual(
            response.status_code, 404
        )

    def test_non_waiting_order(self):
        """
        Make sure it's not possible to update orders with non waiting status.
        """
        self.login(self.user.auth_token.key)
        order = Order.objects.create(user=self.user, total_price=0, status='p')
        response = self.client.patch(self.url(order.id), {'location': 'a'})
        self.assertEqual(
            response.status_code, 400
        )

        self.assertEqual(
            Order.objects.get(id=order.id).location, 'i'
        )

    def test_waiting_order_update(self):
        """
        Make sure users can update waiting orders (only location field).
        """
        self.login(self.user.auth_token.key)
        order = Order.objects.create(total_price=0, user=self.user)
        data = {'location': 'a',
                'status': 'sth',
                'user_id': 4,
                'total_price': '134'}
        response = self.client.patch(self.url(order.id), data)

        updated_order = Order.objects.get(id=order.id)

        self.assertEqual(
            response.status_code, 200
        )
        self.assertEqual(
            updated_order.location, 'a'
        )

        self.assertEqual(
            updated_order.total_price, 0
        )

        self.assertEqual(
            updated_order.user, self.user
        )

        self.assertEqual(
            updated_order.status, 'w'
        )

    def test_non_waiting_database_queries(self):
        """
        Make sure unauthorized updates have fewer queries.
        """
        self.login(self.user.auth_token.key)
        order = Order.objects.create(total_price=0, user=self.user, status='r')

        with self.assertNumQueries(2):
            self.client.patch(self.url(order.id), {'location': 'a'})

    def test_update_waiting_order_database_queries(self):
        """
        Check database queries for update waiting order.
        """
        self.login(self.user.auth_token.key)

        with self.assertNumQueries(3):
            self.client.patch(self.url(self.order.id), {'location': 'a'})


class OrderDeleteViewTest(BaseOrderViewTest):
    """
    Make core.api.views.OrderView works with DELETE requests.
    """
    def test_for_non_waiting_order(self):
        order = Order.objects.create(
            user=self.user,
            total_price=0,
            status='p'
        )

        self.login(token=self.user.auth_token.key)

        response = self.client.delete(self.url(order.id))
        self.assertEqual(
            response.status_code, 404
        )

        self.assertTrue(
            Order.objects.filter(id=order.id).exists()
        )

    def test_for_waiting_order(self):
        order = Order.objects.create(
            user=self.user,
            total_price=0,
        )

        self.login(token=self.user.auth_token.key)

        response = self.client.delete(self.url(order.id))
        self.assertEqual(
            response.status_code, 204
        )

        self.assertFalse(
            Order.objects.filter(id=order.id).exists()
        )

    def test_database_queries(self):
        self.login(token=self.user.auth_token.key)
        o1 = Order.objects.create(
            user=self.user,
            total_price=0
        )

        # Test database queries for a waiting order.
        with self.assertNumQueries(4):
            """
            It should done in 4 queries.
            - user authentication
            - find order
            - delete order
            - deleted related products
            """
            self.client.delete(self.url(o1.id))

        o2 = Order.objects.create(
            user=self.user,
            total_price=0,
            status='p'
        )

        # Test database queries for a non waiting order.
        with self.assertNumQueries(2):
            """
            It should done in 2 queries.
            - user authentication
            - find order
            """
            self.client.delete(self.url(o2.id))


class BaseOrderProductViewTest(APITestCase, AuthTokenCredentialsMixin):
    """
    core.api.OrderProductView handles Patch/Delete Http methods.
    We want to test methods in different test classes.
    This class contains some general cases and helper method.
    """

    fixtures = ['products']
    url_namespace = 'api:order-product'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='foo@email.com',
            username='foo@email.com',
            password='Abc123456789',
        )

        cls.product = Product.objects.first()
        cls.order = Order.objects.create(
            user=cls.user,
            total_price=0
        )

        cls.op = OrderProduct.objects.create(
            order=cls.order,
            product=cls.product,
            customization=cls.product.items[0],
            price=cls.product.price
        )

    def test_authentication(self):
        """
        Make sure authentication is required.
        """

        response = self.client.patch(self.url(self.order.id, self.product.id))
        self.assertEqual(
            response.status_code, 401
        )

    def test_url(self):
        """
        Make sure url connected to view properly.
        """
        response = self.client.patch(self.url(1, 1))
        self.assertEqual(
            response.resolver_match.func.__name__,
            views.OrderProductView.as_view().__name__
        )

    def url(self, *args):
        return reverse(self.url_namespace, args=args)


class OrderProductUpdateViewTest(BaseOrderProductViewTest):

    def test_update(self):
        """
        Make sure view can update a product customization.
        """
        self.order.status = 'w'
        self.order.save()

        self.login(token=self.user.auth_token.key)

        response = self.client.patch(self.url(self.order.id, self.product.id),
                                     {'customization': self.product.items[1]})

        self.assertEqual(
            response.status_code, 200
        )

        self.assertEqual(
            OrderProduct.objects.get(product=self.product, order=self.order).customization,
            self.product.items[1]
        )

    def test_update_with_non_waiting_order(self):
        """
        Make sure cannot change an order that belongs to non waiting order.
        """

        self.order.status = 'r'
        self.order.save()

        self.login(token=self.user.auth_token.key)

        response = self.client.patch(self.url(self.order.id, self.product.id),
                                     {'customization': self.product.items[1]})
        # The view should prevents update orders with non waiting status.
        self.assertEqual(
            response.status_code, 400
        )

        # make sure it's not updated in db.
        self.assertEqual(
            OrderProduct.objects.first().customization, self.product.items[0]
        )


class OrderProductDeleteViewTest(BaseOrderProductViewTest):
    def test_response(self):
        self.login(token=self.user.auth_token.key)

        response = self.client.delete(self.url(self.order.id, self.product.id))

        self.assertEqual(response.status_code, 204)

    def test_deletion(self):
        self.login(token=self.user.auth_token.key)

        self.client.delete(self.url(self.order.id, self.product.id))

        self.assertEqual(
            OrderProduct.objects.count(), 0
        )

    def test_non_waiting_order(self):
        self.login(token=self.user.auth_token.key)

        order = Order.objects.create(
            user=self.user,
            total_price=0,
            status='p'
        )

        response = self.client.delete(self.login(order.id, self.product.id))

        self.assertEqual(
            response.status_code, 404
        )

    def test_total_price(self):
        """
        Make sure Order.total_price will update after remove product to order.
        """
        self.login(token=self.user.auth_token.key)

        order = Order.objects.create(
            user=self.user,
            total_price=7,
            status='w'
        )
        p1 = Product.objects.first()
        p2 = Product.objects.get(title='Tea')
        OrderProduct.objects.create(
            product=p1,
            order=order,
            price=p1.price,
            customization=p1.items[0]
        )

        OrderProduct.objects.create(
            product=p2,
            order=order,
            price=p2.price
        )
        self.client.delete(self.url(order.id, p1.id))

        # make sure price updates with stored price, not original product.
        p1.price = 100
        p1.save()

        self.assertEqual(
            Order.objects.get(id=order.id).total_price, 2
        )

    def test_db_queries(self):
        self.login(token=self.user.auth_token.key)

        with self.assertNumQueries(5):
            """
            It should be done in 3 queries:
            - user authentication
            - find OrderProduct object
            - delete it
            - update Order.total price
            - core.orders.models.remove_empty_orders receiver.
            """
            self.client.delete(self.url(self.order.id, self.product.id))


class OrderProductViewDatabaseQueriesTest(BaseOrderProductViewTest):
    def test_with_non_waiting_order(self):
        self.login(token=self.user.auth_token.key)
        self.order.status = 'p'
        self.order.save()

        with self.assertNumQueries(2):
            """
            It should be done with 2 queries:
            user authentication and find OrderProduct object.
            """
            self.client.patch(self.url(self.order.id, self.product.id), {
                'customization': self.product.items[1]})

    def test_update(self):
        self.order.status = 'w'
        self.order.save()
        self.login(token=self.user.auth_token.key)

        with self.assertNumQueries(3):
            """
            It should be done with 3 queries:
            user authentication and find OrderProduct object.
            update object.
            """
            self.client.patch(self.url(self.order.id, self.product.id), {
                'customization': self.product.items[1]})
