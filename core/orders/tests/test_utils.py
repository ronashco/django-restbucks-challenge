from django.test import TestCase
from django.contrib.auth import get_user_model
from core.orders.models import Cart, Order, OrderProduct
from core.products.models import Product
from .. import utils

User = get_user_model()


class UserCartDetailTest(TestCase):
    """
    Make sure core.orders.utils.user_cart_detail works well.
    """
    fixtures = ['products']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='foo@email.com',
                                            password='Abcd123456789',
                                            email='foo@email.com')
        product = Product.objects.first()
        Cart.objects.create(product=product,
                            user=cls.user,
                            customization=product.items[0])

        Cart.objects.create(product=Product.objects.get(title='Tea'),
                            user=cls.user)

    def test_result_type(self):
        """
        Make sure it returns a tuple with 3 members.
        :return:
        """
        carts = Cart.objects.all()
        self.assertIsInstance(
            utils.user_cart_detail(carts), tuple
        )
        self.assertEqual(3, len(utils.user_cart_detail(carts)))

    def test_products_have_selected_item_attribute(self):
        """
        Make sure adds a selected_item to every single product.
        :return:
        """
        count, total_price, products = utils.user_cart_detail(Cart.objects.all())

        self.assertTrue(
            all([hasattr(p, 'selected_item') for p in products])
        )

    def test_total_price(self):
        """
        Make sure calculates Cart.total_price properly.
        :return:
        """
        carts = Cart.objects.select_related('product').all()
        result = 0
        for cart in carts:
            result += cart.product.price

        self.assertEqual(
            result, utils.user_cart_detail(Cart.objects.all())[1]
        )

    def test_count(self):
        carts = Cart.objects.all()
        self.assertEqual(
            len(carts), utils.user_cart_detail(carts)[0]
        )

    def test_executed_queries(self):
        """
        Make sure it doesnt execute any query.
        """
        carts = Cart.objects.select_related('product').all()
        # because django query sets are lazy, we want to execute query,
        # and then call definition.
        len(carts)  # Through call len on a query set, the query will executes.
        with self.assertNumQueries(0):
            utils.user_cart_detail(carts)


class MergeCartToOrderTest(TestCase):
    """
    Make sure core.orders.utils.merge_cart_to_order works well.
    """
    fixtures = ['products']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='foo@email.com',
                                            password='Abcd123456789',
                                            email='foo@email.com')
        product = Product.objects.first()
        Cart.objects.create(product=product,
                            user=cls.user,
                            customization=product.items[0])

        Cart.objects.create(product=Product.objects.get(title='Tea'),
                            user=cls.user)

    def test_returns_tuple(self):
        """
        Make sure it returns a tuple with 2 members.
        """
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        result = utils.merge_cart_to_order(order)

        self.assertIsInstance(
            result, tuple
        )

        self.assertEqual(
            2, len(result)
        )

    def test_removes_cart_objects(self):
        """
        Make sure it removes associated carts.
        """
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        utils.merge_cart_to_order(order)

        self.assertFalse(
            Cart.objects.filter(user=self.user).exists()
        )

    def test_creates_order_products(self):
        """
        Make sure it creates a OrderProduct object for every single Cart object.
        """
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        except_count = Cart.objects.filter(user=self.user).count()
        utils.merge_cart_to_order(order)

        self.assertEqual(
            OrderProduct.objects.count(),
            except_count
        )

    def test_total_price_value(self):
        """
        Make sure it calculates total price properly.
        """
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        result = 0
        for cart in Cart.objects.select_related('product').all():
            result += cart.product.price

        total_price, _ = utils.merge_cart_to_order(order)

        self.assertEqual(
            total_price, result
        )

    def test_order_product(self):
        """
        Make sure it returns an iterable of OrderProduct objects.
        """
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        _, order_products = utils.merge_cart_to_order(order)

        for op in order_products:
            self.assertIsInstance(op, OrderProduct)

    def test_executed_queries(self):
        order = Order.objects.create(user=self.user,
                                     total_price=0)

        with self.assertNumQueries(3):
            utils.merge_cart_to_order(order)
