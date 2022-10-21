from django.contrib import admin
from .models import Promo, Category, Product, Image

# Register your models here.
admin.site.register(Promo)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)