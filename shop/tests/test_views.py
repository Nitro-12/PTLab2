from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, PromoCode, Purchase

class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем товары и промокоды для тестов
        self.product1 = Product.objects.create(name="Компьютер RTX-strike", price=50000)
        self.product2 = Product.objects.create(name="Компьютер RTX-strike 2.0", price=1500)
        self.promo = PromoCode.objects.create(code="DISCOUNT10", description="Скидка 10%")
        self.product1.promo_codes.add(self.promo)

    def test_index_view_accessibility(self):
        # Проверка доступности главной страницы
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_all_products_display(self):
        # Проверка отображения всех товаров на странице
        response = self.client.get(reverse('index'))
        self.assertContains(response, "Компьютер RTX-strike")
        self.assertContains(response, "Компьютер RTX-strike 2.0")

    def test_valid_promo_code_applies_products(self):
        # Проверка привязанных к промокоду, отображаются
        response = self.client.get(reverse('index') + '?promo_code=DISCOUNT10')
        self.assertContains(response, "Компьютер RTX-strike")  # Товар, связанный с промокодом
        self.assertContains(response, "Компьютер RTX-strike 2.0")
        self.assertIn("Промокод 'DISCOUNT10' применен", response.context['message'])

    def test_invalid_promo_code(self):
        # При введении неверного промокода
        response = self.client.get(reverse('index') + '?promo_code=INVALID')
        self.assertContains(response, "Неверный промокод.")
        self.assertContains(response, "Компьютер RTX-strike")
        self.assertContains(response, "Компьютер RTX-strike 2.0")
        self.assertEqual(len(response.context['promo_products']), 0)  #Проверка осустсвия промокода

class PurchaseCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Компьютер RTX-strike 3.0", price=30000)

    def test_purchase_create_accessibility(self):
        # Доступность страницы для создания покупки
        response = self.client.get(reverse('buy', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_valid_purchase_submission(self):
        # Покупка успешно создается
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'product': self.product.id,
            'person': "Пётр Петров",
            'address': "Богунская, д.10"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо за покупку, Пётр Петров!")
        # Покупка была сохранена в базе
        purchase = Purchase.objects.get(person="Пётр Петров")
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.address, "Богунская, д.10")
