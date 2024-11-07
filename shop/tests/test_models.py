from django.test import TestCase
from shop.models import Product, Purchase, PromoCode
from datetime import datetime


class PromoCodeTestCase(TestCase):
    def setUp(self):
        PromoCode.objects.create(code="DISCOUNT10", description="10% Discount")
        PromoCode.objects.create(code="NEWYEAR", description="New Year Sale")

    def test_correctness_types(self):
        discount_code = PromoCode.objects.get(code="DISCOUNT10")
        newyear_code = PromoCode.objects.get(code="NEWYEAR")

        self.assertIsInstance(discount_code.code, str)
        self.assertIsInstance(discount_code.description, str)
        self.assertIsInstance(newyear_code.code, str)
        self.assertIsInstance(newyear_code.description, str)

    def test_correctness_data(self):
        discount_code = PromoCode.objects.get(code="DISCOUNT10")
        newyear_code = PromoCode.objects.get(code="NEWYEAR")

        self.assertEqual(discount_code.description, "10% Discount")
        self.assertEqual(newyear_code.description, "New Year Sale")


class ProductTestCase(TestCase):
    def setUp(self):
        self.promo1 = PromoCode.objects.create(code="SUMMER", description="Summer Sale")
        self.promo2 = PromoCode.objects.create(code="WINTER", description="Winter Sale")

        self.product1 = Product.objects.create(name="laptop", price=50000)
        self.product2 = Product.objects.create(name="mouse", price=1000)

        # Add promo codes to products
        self.product1.promo_codes.set([self.promo1, self.promo2])
        self.product2.promo_codes.add(self.promo1)

    def test_correctness_types(self):
        self.assertIsInstance(self.product1.name, str)
        self.assertIsInstance(self.product1.price, int)
        self.assertIsInstance(self.product2.name, str)
        self.assertIsInstance(self.product2.price, int)

    def test_correctness_data(self):
        self.assertEqual(self.product1.price, 50000)
        self.assertEqual(self.product2.price, 1000)
        self.assertIn(self.promo1, self.product1.promo_codes.all())
        self.assertIn(self.promo2, self.product1.promo_codes.all())
        self.assertIn(self.promo1, self.product2.promo_codes.all())
        self.assertNotIn(self.promo2, self.product2.promo_codes.all())


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.promo = PromoCode.objects.create(code="DISCOUNT20", description="20% Discount")
        self.product = Product.objects.create(name="tablet", price=30000)
        self.product.promo_codes.add(self.promo)
        self.datetime = datetime.now()

        self.purchase = Purchase.objects.create(
            product=self.product,
            person="Petrov",
            address="Lenina St."
        )

    def test_correctness_types(self):
        self.assertIsInstance(self.purchase.person, str)
        self.assertIsInstance(self.purchase.address, str)
        self.assertIsInstance(self.purchase.date, datetime)

    def test_correctness_data(self):
        self.assertEqual(self.purchase.person, "Petrov")
        self.assertEqual(self.purchase.address, "Lenina St.")
        # Test date ignoring microseconds for accuracy
        self.assertEqual(self.purchase.date.replace(microsecond=0), self.datetime.replace(microsecond=0))

    def test_product_promo_codes(self):
        # Ensure the promo code is correctly linked to the purchased product
        self.assertIn(self.promo, self.product.promo_codes.all())
