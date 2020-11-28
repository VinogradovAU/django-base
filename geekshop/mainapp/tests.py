from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainappTestCase(TestCase):
    expected_success_code = 200

    def setUp(self):
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'db.json')
        self.client = Client()

    def test_mainapp_urls(self, expected_success_code=200):
        response = self.client.get('/')
        self.assertEqual(response.status_code, expected_success_code)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, expected_success_code)

        response = self.client.get('/products/category/0/page/1')
        self.assertEqual(response.status_code, expected_success_code)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/page/1')
            self.assertEqual(response.status_code, expected_success_code)

        for pk in range(1, 8):
            response = self.client.get(f'/products/category/0/page/{pk}')
            self.assertEqual(response.status_code, expected_success_code)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp',\
    #                  'basketapp')


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="стулья")
        self.product_1 = Product.objects.create(name="стул 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="стул 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="стул 3",
                                                category=category,
                                                price=998.1,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="стул 1")
        product_2 = Product.objects.get(name="стул 2")
        self.assertEqual(str(product_1), 'стул 1 (стулья)')
        self.assertEqual(str(product_2), 'стул 2 (стулья)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="стул 1")
        product_3 = Product.objects.get(name="стул 3")
        products = Product.objects.all()

        self.assertEqual(list(products), [product_1, product_3])
