from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Product, Purchase, PromoCode


def index(request):
    # Получаем все товары по умолчанию
    all_products = Product.objects.all()

    # Проверяем, был ли введен промокод
    promo_code = request.GET.get('promo_code')
    promo_products = []  # Список для товаров, добавляемых по промокоду
    message = "Введите промокод, чтобы увидеть дополнительные товары."

    # Если введен промокод, проверяем его наличие
    if promo_code:
        try:
            promo = PromoCode.objects.get(code=promo_code)
            # Получаем товары, привязанные к промокоду
            promo_products = promo.products.all()
            message = f"Промокод '{promo_code}' применен. Добавлены дополнительные товары."
        except PromoCode.DoesNotExist:
            message = "Неверный промокод."

    context = {
        'all_products': all_products,  # Все товары по умолчанию
        'promo_products': promo_products,  # Товары, добавляемые по промокоду
        'message': message,
    }

    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['product', 'person', 'address']

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f'Спасибо за покупку, {self.object.person}!')
