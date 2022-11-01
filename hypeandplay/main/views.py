from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from . import serializer
from rest_framework.response import Response
from .filters import ProductFilter

from drf_spectacular.utils import extend_schema

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

    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category",'stock', 'price']
    search_fields = ['name']
    ordering_fields = ("price",)
    
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
        
        res_img = []
        for image in images:
            img = models.Image.objects.create(image = image, product_id = product)
            res_img.append(img.__str__())
            img.save()
        
        data['images'] = res_img
        data['product']['id'] = product.id
        
        return Response(data)
    
    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.serializer_class["default"])

