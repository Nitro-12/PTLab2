from django.contrib import admin
from .models import Product, PromoCode, Purchase

# Регистрация модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Колонки для отображения в списке
    search_fields = ('name',)  # Поле для поиска по наименованию
    list_filter = ('price',)  # Фильтры для цены

# Регистрация модели PromoCode
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')  # Колонки для отображения промокодов
    search_fields = ('code',)  # Поиск по коду промокода

# Регистрация модели Purchase
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'person', 'address', 'date')  # Колонки для отображения покупок
    search_fields = ('person',)  # Поиск по имени покупателя
    list_filter = ('date',)  # Фильтр по дате

# Регистрация моделей
admin.site.register(Product, ProductAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
