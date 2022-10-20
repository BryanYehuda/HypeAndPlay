from django.contrib import admin
from .models import Promo, Category, Product

# Register your models here.
admin.site.register(Promo)
admin.site.register(Category)
admin.site.register(Product)