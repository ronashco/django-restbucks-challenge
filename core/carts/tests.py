from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core.products.models import Product
from .models import Cart, CartApiModel

User = get_user_model()


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
