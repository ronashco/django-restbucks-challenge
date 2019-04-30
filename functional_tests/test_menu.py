from django.test import LiveServerTestCase


class TestProductList(LiveServerTestCase):
    """
    Make sure our menu works well.
    """
    def test_contains_primary_data(self):
        response = self.client.get('/api/products/')
        for p in response.json():
            self.assertEqual(
                {'title', 'price', 'options'}, set(p.keys())
            )
