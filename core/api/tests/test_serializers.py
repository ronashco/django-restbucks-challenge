from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase
from core.products.models import Product
from core.orders.models import (
    Cart, Order, OrderProduct, OrderProductApiModel
)
from core.accounts.tests import AuthTokenCredentialsMixin
from .. import serializers

User = get_user_model()


class TestProductListSerializer(TestCase):
    fixtures = ['products']

    def setUp(self):
        self.serializer_class = serializers.ProductListSerializer

    def test_fields(self):
        """Make sure serializer data contains primary product's columns"""
        instance = self.serializer_class(instance=Product.objects.first())
        self.assertEqual(
            {'title', 'price', 'option', 'items', 'id'}, set(instance.data.keys())
        )

    def test_items(self):
        """Make sure items converted to python's list"""
        instance = self.serializer_class(instance=Product.objects.first())
        self.assertIsInstance(
            instance.data['items'], list
        )

    def test_collection(self):
        products = Product.objects.all()

        result = [OrderedDict({'title': p.title, 'price': p.price,
                               'option': p.option, 'items': p.items, 'id': p.id})
                  for p in products]
        self.assertEqual(
            self.serializer_class(products, many=True).data, result
        )


class RegisterSerializerTest(TestCase):
    class TestRegistrationSerializer(TestCase):
        @classmethod
        def setUpTestData(cls):
            cls.user = User.objects.create_user(username='foo@email.com',
                                                email='foo@email.com',
                                                password='Aa12456789')
            cls.serializer = serializers.RegisterSerializer(instance=cls.user)

        def test_fields(self):
            """
            Password field must be read only, so serializer data contains only email field.
            """
            self.assertEqual(
                {'email'}, set(self.serializer.data.keys())
            )

        def test_email_validation(self):
            """
             Make sure the email validator checks for email's uniqueness/pattern.
            """
            invalid_serializer = serializers.RegisterSerializer(data={'email': 'foo@email.com',
                                                                      'password': 'Abc12345678'})
            self.assertFalse(
                invalid_serializer.is_valid()
            )

            invalid_serializer = serializers.RegisterSerializer(data={'password': 'Abc12345678'})
            self.assertFalse(invalid_serializer.is_valid())

            invalid_serializer = serializers.RegisterSerializer(data={'email': 'valid@email.com'})
            self.assertFalse(invalid_serializer.is_valid())

            valid_serializer = serializers.RegisterSerializer(data={'email': 'valid@email.com',
                                                                    'password': 'Abc12345678'})
            self.assertTrue(
                valid_serializer.is_valid()
            )

        def test_password_validation(self):
            """
            Make sure the password validator doesnt accept passwords that contains
            less than 8 letters.
            """
            s = serializers.RegisterSerializer(data={'email': 'john@email.com',
                                                     'password': '1234567'})
            self.assertFalse(
                s.is_valid()
            )

        def test_save(self):
            """
            Make sure serializer stores data correctly,
            e.g. doesnt store raw password.
            """
            data = {'email': 'johndoe@email.com',
                    'password': 'Abc123456789'}
            serializer = serializers.RegisterSerializer(data=data)
            serializer.save()

            self.assertNotEqual(
                data['password'], serializer.instance.password
            )


class ShowCartsSerializerTest(TestCase):
    def setUp(self):
        self.serializer_class = serializers.ShowCartsSerializer

    def test_fields(self):
        self.assertEqual({'count', 'total_price', 'products'},
                         set(self.serializer_class().fields.keys()))

    def test_product_fields(self):
        self.assertEqual({'title', 'price', 'option', 'selected_item', 'id'},
                         set(self.serializer_class.CartProductSerializer().fields.keys()))


class CartSerializerTest(APITestCase, AuthTokenCredentialsMixin):
    """
    Test core.api.serializers.CartSerializer
    """
    fixtures = ['products']

    def setUp(self):
        self.serializer_class = serializers.CartSerializer

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )

    def test_fields(self):
        self.assertEqual(
            {'product', 'user', 'customization'}, set(self.serializer_class().fields)
        )

    def test_validation(self):
        """Make sure serializer applies model level validations."""

        #  Prepare request object.
        self.login(token=self.user.auth_token.key)
        response = self.client.post(reverse('api:cart'))

        product = Product.objects.get(title='Tea')
        s = self.serializer_class(data={'product': product.id, 'customization': 'sth ...'},
                                  context={'request': response.wsgi_request})
        # The product does not support customization.
        with self.assertRaises(ValidationError):
            s.is_valid(raise_exception=True)

    def test_create(self):
        """Make sure serializer has ability to create Order object."""

        self.login(token=self.user.auth_token.key)
        response = self.client.post(reverse('api:cart'))

        product = Product.objects.first()
        s = self.serializer_class(data={'product': product.id,
                                        'user': self.user.id,
                                        'customization': product.items[0]},
                                  context={'request': response.wsgi_request})

        s.is_valid()

        self.assertIsInstance(s.save(), Cart)
        self.assertEqual(1, Cart.objects.count())


class OrderListSerializerTest(TestCase):
    fixtures = ['products']

    def setUp(self):
        self.serializer_class = serializers.OrderListSerializer

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )
        Order.objects.create(user=user, total_price=0)
        Order.objects.create(user=user, total_price=0)

    def test_fields(self):
        self.assertEqual(
            set(self.serializer_class().fields), {'id', 'status', 'date', 'location', 'user', 'total_price'}
        )

    def test_data(self):
        s = self.serializer_class(Order.objects.values('id', 'date', 'status'), many=True)
        self.assertEqual(2, len(s.data))

    def test_read_only_fields(self):
        s = self.serializer_class(Order.objects.values('id', 'date', 'status'), many=True)
        for p in s.data:
            self.assertNotIn('location', p)


class OrderSerializerTest(TestCase):
    fixtures = ['products']

    def setUp(self):
        self.serializer_class = serializers.OrderSerializer

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='m@email.com',
            email='m@email.com',
            password='Abc123456789',
        )
        cls.order = Order.objects.create(user=cls.user, total_price=0)
        product = Product.objects.first()
        OrderProduct.objects.create(product=product,
                                    order=cls.order,
                                    customization=product.items[0],
                                    price=product.price)

    def test_fields(self):
        serializer = self.serializer_class()
        self.assertEqual(
            {'total_price', 'status', 'location', 'date', 'products'},
            set(serializer.fields)
        )

    def test_serialization(self):
        """
        Make sure order serializer represents data properly.
        :return:
        """
        order = Order.objects.prefetch_related('products', 'orderproduct_set').first()
        with self.assertRaises(AttributeError):
            """
            Every Order object that used to initialize serialize, 
            should has a order_product attribute.
           """
            _ = self.serializer_class(order).data

        order_products = [OrderProductApiModel(title=op.product.title,
                                               price=op.price,
                                               option=op.product.option,
                                               item=op.customization, id_=op.product.id)
                          for op in order.orderproduct_set.all()]

        order.order_products = order_products

        data = self.serializer_class(order).data
        self.assertEqual(
            data['total_price'], order.total_price
        )
        self.assertEqual(
            data['status'], order.status
        )

        self.assertEqual(
            data['location'], order.location
        )
        self.assertEqual(
            data['date'], order.date.strftime("%d %b %Y-%H:%M")
        )

        for p in order_products:
            d = {
                'title': p.title,
                'price': p.price,
                'option': p.option,
                'item': p.item,
                'id': p.id,
            }
            self.assertIn(OrderedDict(d), data['products'])

    def test_update(self):
        """
        Make sure we can use serializer in update order api.
        :return:
        """
        serializer = self.serializer_class(instance=self.order,
                                           data={'location': 'a', 'status': 'p'},
                                           partial=True)
        serializer.is_valid()
        serializer.save()

        #  Make sure location is writable.
        self.assertEqual(
            serializer.instance.location, 'a'
        )

        #  Make sure status is read only.
        self.assertEqual(
            serializer.instance.status, 'w'
        )

    def tests_validation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=0,
            status='r',
            location='a'
        )

        serializer = serializers.OrderSerializer(instance=order, data={'location': 'i'}, partial=True)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
