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
        
        images = request.data.pop('images', [])
        
        data = {
            "images" : images,
            "product" : request.data
        }
        
        serial = self.get_serializer(data=data)
        serial.is_valid(raise_exception=True)
    
        input_prod = {**serial.data['product']}
        
        cat = models.Category.objects.get(id=int(input_prod['category']))
        input_prod['category'] = cat
        
        promos = input_prod.pop("promo") 
        
        product = models.Product.objects.create(**input_prod)
        product.save()
        
        for promo in promos:
            prom = models.Promo.objects.get(id=int(promo))
            product.promo.add(prom)
        
        product.save()
        
        for image in images:
            img = models.Image.objects.create(image = image, product_id = product)
            img.save()
        
        return Response(serial.data)
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.serializer_class["default"])

