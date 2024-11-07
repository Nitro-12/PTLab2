from django.db import models

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    promo_codes = models.ManyToManyField(PromoCode, blank=True, related_name='products')

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
