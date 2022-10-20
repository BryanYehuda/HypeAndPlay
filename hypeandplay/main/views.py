from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer
from rest_framework.response import Response
import uuid

# Create your views here.


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = serializer.CategorySerializer
    queryset = models.Category.objects.all()


class PromoViewset(viewsets.ModelViewSet):
    serializer_class = serializer.PromoSerializer
    queryset = models.Promo.objects.all()


class ProductViewset(viewsets.ModelViewSet):
    serializer_class = {
        "create": serializer.ProductImageSerializer,
        "default": serializer.ProductSerializer,
    }

    queryset = models.Product.objects.all()

    def create(self, request, *args, **kwargs):
        images = request.data.pop("images")
        
        print(images)
        
        return super().create(request, *args, **kwargs)
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.serializer_class["default"])

