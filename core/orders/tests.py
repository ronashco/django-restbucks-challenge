from django.test import TestCase
from django.contrib.auth import get_user_model
from core.products.models import Product
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .models import Order, OrderProduct

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

        order = Order.objects.create(user=self.user, location='a')

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
            unit_price=self.product.price,
        )
        self.assertIsInstance(
            self.order.products.first(), OrderProduct
        )
        self.assertEqual(1, OrderProduct.objects.count())

    def test_save_method_runs_validations(self):
        """Make sure OrderProduct.save calls OrderProduct.clean before save object"""
        obj = OrderProduct(order=self.order, product=self.product,
                           customization='Oops', unit_price=self.product.price,
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
                unit_price=self.product.price
            )

            self.order.products.create(
                product=self.product,
                unit_price=self.product.price,
                customization='invalid.'
            )

        product = Product.objects.get(title='Tea')
        with self.assertRaises(ValidationError):
            self.order.products.create(
                product=product,
                unit_price=product.price,
                customization='invalid.'
            )

    def test_count_default_value(self):
        """
        Make sure object has one count by default.
        """
        order_product = self.order.products.create(
            product=self.product,
            customization=self.product.items[0],
            unit_price=self.product.price,
        )
        self.assertEqual(
            order_product.count, 1
        )

    def test_uniqueness(self):
        """
        Make sure product and order fields are unique together.
        """
        self.order.products.create(
            product=self.product,
            customization=self.product.items[0],
            unit_price=self.product.price,
        )
        with self.assertRaises(IntegrityError):
            self.order.products.create(
                product=self.product,
                customization=self.product.items[0],
                unit_price=self.product.price,
            )
