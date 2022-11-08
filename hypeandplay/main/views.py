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
    
    def list(self, request, *args, **kwargs):
        
        child = self.get_child(0)
        res = {'result' : child}
        
        return Response(res)

    def  get_child(self, ids : int):
        result = {}
        q = models.Category.objects.filter(parent_category = ids).all()
        res = []
        if len(q) == 0:
            return res
        for i in q:
            child = self.get_child(i.id)
            result = {"category" : i.name_category, "child" : child, "id" : i.id}
            res.append(result)
        return res
               

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
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class AdBannerViewset(viewsets.ModelViewSet):
    queryset = models.AdBanner.objects.all()
    serializer_class = serializer.AdBannerSerializer