from datetime import datetime
from django.test import TestCase
from . import models


class TestProductModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = models.Product.objects.create(
            title='Latte',
            price='5',
            option='Milk',
            items=['skim', 'semi', 'whole']
        )

    def test_creation(self):
        """Make sure product object created properly."""
        self.assertIsInstance(
            self.product, models.Product
        )
        self.assertEqual(1, models.Product.objects.count())

    def test_create_dates(self):
        """
        Make sure the create_date field sets automatically.
        """
        self.assertEquals(
            datetime.now().date(), self.product.create_date.date(),
            self.product.update_date.date()
        )

    def test_items(self):
        self.assertIsInstance(
            self.product.items, list
        )

    def test_nullable_fields(self):
        """Make sure we can have a product without option/items"""
        product = models.Product.objects.create(
            title='Cake',
            price=2,
        )

        self.assertIsNone(product.option)
        self.assertIsNone(product.items)
