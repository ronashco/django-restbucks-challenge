from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.products.models import Product
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import Order, OrderProduct, Cart, CartApiModel

User = get_user_model()


class BaseOrderTest(TestCase):
    """
    Basic configurations for test order app models.
    """
    fixtures = ['products']

    def setUp(self):
        # Reset order status to waiting.
        self.order.status = 'w'
        self.order.save()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='foo@email.com',
                                            email='foo@email.com',
                                            password='Abc123456789')
        cls.order = Order.objects.create(
            user=cls.user,
            total_price=0
        )


class OrderModelTest(BaseOrderTest):
    """
    Test core.orders.Order model.
    """
    def test_creation(self):
        self.assertIsInstance(
            self.order, Order
        )

        self.assertEqual(1, Order.objects.count())

    def test_default_values(self):
        self.assertEqual('w', self.order.status)
        self.assertEqual('i', self.order.location)

    def test_str(self):
        self.assertEquals(
            str(self.order), "%s (%s)" % (self.order.status_label, str(self.order.date.date()))
        )

    def test_change_status_validation(self):
        """
        Make sure Order._change_status prevents invalid changes.
        """
        self.order._change_status('invalid')
        self.assertEqual(
            self.order.status, 'w'
        )
        self.order._change_status('r')
        self.assertEqual(
            self.order.status, 'r'
        )

    def test_status_helper_methods(self):
        self.order.prepare()
        self.assertEqual(
            self.order.status, 'p'
        )

        self.order.ready()
        self.assertEqual(
            self.order.status, 'r'
        )

        self.order.deliver()
        self.assertEqual(
            self.order.status, 'd'
        )

    def test_status_label(self):
        self.assertEqual(
            self.order.status_label, 'Waiting'
        )

        self.order.prepare()
        self.assertEqual(
            self.order.status_label, 'Preparation'
        )

        self.order.ready()
        self.assertEqual(
            self.order.status_label, 'Ready'
        )

        self.order.deliver()
        self.assertEqual(
            self.order.status_label, 'Delivered'
        )

    def test_location_label(self):
        self.assertEqual(
            self.order.location_label, 'In shop'
        )

        order = Order.objects.create(user=self.user, total_price=0, location='a')

        self.assertEqual(
            order.location_label, 'Away'
        )


class TestOrderProductModel(BaseOrderTest):
    """
    Test core.orders.OrderProduct model.
    """
    @classmethod
    def setUpTestData(cls):
        super(TestOrderProductModel, cls).setUpTestData()
        cls.product = Product.objects.first()

    def test_creation(self):
        """
        Make sure relation ship and related_name works well.
        """
        self.order.products.create(
            product=self.product,
            customization=self.product.items[0],
            price=self.product.price,
        )
        self.assertIsInstance(
            self.order.products.first(), OrderProduct
        )
        self.assertEqual(1, OrderProduct.objects.count())

    def test_save_method_runs_validations(self):
        """Make sure OrderProduct.save calls OrderProduct.clean before save object"""
        obj = OrderProduct(order=self.order, product=self.product,
                           customization='Oops', price=self.product.price,
                           )
        with self.assertRaises(ValidationError):
            obj.save()

    def test_customization_validation(self):
        """
        Make sure customization field in based on product customization.
        """
        with self.assertRaises(ValidationError):
            self.order.products.create(
                product=self.product,
                price=self.product.price
            )

            self.order.products.create(
                product=self.product,
                price=self.product.price,
                customization='invalid.'
            )

        product = Product.objects.get(title='Tea')
        with self.assertRaises(ValidationError):
            self.order.products.create(
                product=product,
                price=product.price,
                customization='invalid.'
            )

    def test_uniqueness(self):
        """
        Make sure product and order fields are unique together.
        """
        self.order.products.create(
            product=self.product,
            customization=self.product.items[0],
            price=self.product.price,
        )
        with self.assertRaises(IntegrityError):
            self.order.products.create(
                product=self.product,
                customization=self.product.items[0],
                price=self.product.price,
            )


class TestCartModel(TestCase):
    fixtures = ['products']

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.first()
        cls.user = User.objects.create_user(username='foo@email.com',
                                            password='Abc123456789')
        cls.cart = Cart.objects.create(
            product=cls.product,
            user=cls.user,
            customization=cls.product.items[0]
        )

    def test_creation(self):
        """
        Make sure object created properly.
        """
        self.assertIsInstance(
            self.cart, Cart
        )
        self.assertEqual(
            Cart.objects.count(), 1
        )

    def test_product_instance(self):
        """
        Make sure Cart.product is instance of 'core.products.models.Product'.
        """
        self.assertIsInstance(
            self.cart.product, Product
        )

    def test_user_instance(self):
        """
        Make sure Cart.product is instance of 'django.contrib.auth.models.User'.
        """
        self.assertIsInstance(
            self.cart.user, User
        )

    def test_option_validation(self):
        """
        Make sure clean method (Cart.clean) works well.
        """
        cart = Cart(product=self.product, user=self.user)
        # The product has option (option of the product is not null),
        # so we should pass one item to Cart class.
        with self.assertRaises(ValidationError):
            cart.clean()

        # In this case, the product has no option and
        # we are passing something as option, so the clean method should raises ValidationError
        product = Product.objects.get(title='Tea')
        cart = Cart(product_id=product.id, user=self.user, customization='something')
        with self.assertRaises(ValidationError):
            cart.clean()

        # make sure validation works when we call create method.
        with self.assertRaises(ValidationError):
            Cart.objects.create(product_id=product.id, user=self.user, customization='something')

        # select invalid item
        with self.assertRaises(ValidationError):
            Cart.objects.create(product=self.product, user=self.user, customization='$invalid_item')

    def test_product_on_delete_is_cascade(self):
        """
        Make sure on_delete property is protected for product.
        """
        self.product.delete()
        self.assertFalse(
            Cart.objects.filter(id=self.cart.id).exists()
        )

    def test_user_on_delete_is_cascade(self):
        """
        Make sure on_delete property is cascade for user.
        """
        self.user.delete()
        self.assertFalse(
            Cart.objects.filter(id=self.cart.id).exists()
        )

    def test_date_fields(self):
        """
        Make sure create/update date has current date.
        """
        self.assertEquals(
            self.cart.create_date.date(), self.cart.update_date.date(),
            datetime.now().date()
        )

    def test_customization_can_be_null(self):
        """
        Make sure we can leave customization empty, if product.option is null.
        """
        product = Product.objects.get(title='Tea')
        cart = Cart.objects.create(user=self.user, product=product)
        self.assertIsNone(
            cart.customization
        )

    def test_unique_fields(self):
        """Make sure product and user are unique together"""
        product = Product.objects.create(
            title='Cake',
            price=4,
            option='size',
            items=['small', 'medium', 'large']
        )

        Cart.objects.create(product=product, user=self.user, customization='small')
        with self.assertRaises(ValidationError):
            Cart.objects.create(product=product, user=self.user, customization='small')


class CartApiModelTest(TestCase):
    def setUp(self):
        self.cart_api_model = CartApiModel

    def test_attributes(self):
        obj = self.cart_api_model(count=1, total_price=2, products=[])
        self.assertTrue(
            hasattr(obj, 'count') and obj.count == 1
        )
        self.assertTrue(
            hasattr(obj, 'total_price') and obj.total_price == 2
        )
        self.assertTrue(
            hasattr(obj, 'products') and obj.products == []
        )
