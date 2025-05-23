from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from shop.views import product_list, product_detail, search


class TestUrls(SimpleTestCase):
    def test_product_list(self):
        url = reverse('shop:products')  # products/
        self.assertEqual(resolve(url).func, product_list)

    def test_product_detail(self):
        url = reverse("shop:product_detail", args=(1, 'slug'))
        self.assertEqual(resolve(url).func, product_detail)

    def test_search(self):
        url = reverse('shop:search')
        self.assertEqual(resolve(url).func, search)

