from django.test import TestCase
from ..serializers import ProductListSerializer
from core.products.models import Product


class TestProductListSerializer(TestCase):
    fixtures = ['products']

    def setUp(self):
        self.serializer_class = ProductListSerializer

    def test_fields(self):
        """Make sure serializer data contains primary product's columns"""
        instance = self.serializer_class(instance=Product.objects.first())
        self.assertEqual(
            {'title', 'price', 'option', 'items'}, set(instance.data.keys())
        )

    def test_items(self):
        """Make sure items converted to python's list"""
        instance = self.serializer_class(instance=Product.objects.first())
        self.assertIsInstance(
            instance.data['items'], list
        )

    def test_collection(self):
        from collections import OrderedDict

        products = Product.objects.all()

        result = [OrderedDict({'title': p.title, 'price': p.price, 'option': p.option, 'items': p.items})
                  for p in products]
        self.assertEqual(
            self.serializer_class(products, many=True).data, result
        )
