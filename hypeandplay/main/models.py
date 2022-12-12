from django.db import models
import uuid
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin,Group
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import lazy as _
from django.contrib.auth.base_user import BaseUserManager

def get_image_url(instance, files):
    key = instance.__dict__.keys()
    if "name" in key:
        url = f"image/{instance.name}-{files}"
    elif "product_id_id" in key:
        url = f"image/{instance.product_id}-{files}"
    return url

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)
    avatar = models.ImageField(upload_to=get_image_url, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_items = models.PositiveIntegerField()
    total = models.PositiveBigIntegerField()
