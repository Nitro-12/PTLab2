from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, PromoCode, Purchase

class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем товары и промокоды для тестов
        self.product1 = Product.objects.create(name="Laptop", price=50000)
        self.product2 = Product.objects.create(name="Mouse", price=1500)
        self.promo = PromoCode.objects.create(code="DISCOUNT10", description="10% Discount")
        self.product1.promo_codes.add(self.promo)

    def test_index_view_accessibility(self):
        # Проверяем доступность главной страницы
        response = self.client.get(reverse('index'))  # Замените 'index' на ваш путь
        self.assertEqual(response.status_code, 200)

    def test_all_products_display(self):
        # Проверяем, что все товары отображаются на странице
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Laptop")
        self.assertContains(response, "Mouse")

    def test_valid_promo_code_applies_products(self):
        # Проверяем, что товары, привязанные к промокоду, отображаются
        response = self.client.get(reverse('index') + '?promo_code=DISCOUNT10')
        self.assertContains(response, "Laptop")  # Товар, связанный с промокодом
        self.assertContains(response, "Mouse")   # Все товары отображаются
        self.assertIn("Промокод 'DISCOUNT10' применен", response.context['message'])

    def test_invalid_promo_code(self):
        # Проверяем, что происходит при введении неверного промокода
        response = self.client.get(reverse('index') + '?promo_code=INVALID')
        self.assertContains(response, "Неверный промокод.")
        self.assertContains(response, "Laptop")
        self.assertContains(response, "Mouse")
        self.assertEqual(len(response.context['promo_products']), 0)  # Проверка на отсутствие товаров по неверному промокоду

class PurchaseCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Tablet", price=30000)

    def test_purchase_create_accessibility(self):
        # Проверяем доступность страницы для создания покупки
        response = self.client.get(reverse('buy', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_valid_purchase_submission(self):
        # Проверяем, что покупка успешно создается
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'product': self.product.id,
            'person': "Ivan Ivanov",
            'address': "Main St. 10"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо за покупку, Ivan Ivanov!")
        # Проверяем, что покупка была сохранена в базе
        purchase = Purchase.objects.get(person="Ivan Ivanov")
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.address, "Main St. 10")
