from email.policy import default
from enum import unique
from unittest.util import _MAX_LENGTH
from django.db import models
import uuid

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    password = models.CharField(max_length=255, default = "admin")


class Category(models.Model):
    name_category = models.CharField(max_length=255)
    parent_category = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name_category}"


class Promo(models.Model):
    promo_name = models.CharField(max_length=255)
    promo_desc = models.TextField()

    def __str__(self):
        return f"{self.promo_name}"


class Product(models.Model):
    id = models.UUIDField(default = uuid.uuid1, editable = False, unique = True, primary_key = True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()
    status = models.BooleanField()
    stock = models.PositiveIntegerField()
    new_release = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    promo = models.ManyToManyField(Promo)

    def __str__(self):
        return f"{self.name}"

def get_image_url(instance, files):
    key = instance.__dict__.keys()
    if "name" in key:
        url = f"image/{instance.id}-{files}"
    elif "product_id_id" in key:
        url = f"image/{instance.product_id}-{files}"
    return url

class Image(models.Model):
    image = models.ImageField(upload_to=get_image_url)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}-{self.image}"
    
class AdBanner(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to=get_image_url)
    desc = models.TextField()
    
    def __str__(self):
        return f"{self.name}"
    
class Event(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to=get_image_url)
    desc = models.TextField()

    def __str__(self):
        return f"{self.name}"