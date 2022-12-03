from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Promo, Category, Product, Image, User

# Register your models here.
admin.site.register(Promo)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(User)

