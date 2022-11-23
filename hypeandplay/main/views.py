from django.shortcuts import render
from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from . import serializer
from rest_framework.response import Response
from .filters import ProductFilter
from django.db.models.query import QuerySet

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SignUpViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    serializer_class = serializer.SignUpSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = models.Admin.objects.get_or_create(**data)
        if not user[1]:
            return Response({"result" : "User already exists"})
        return Response({"result" :"User has been created"})

class LoginViewset(viewsets.GenericViewSet):
    serializer_class = serializer.LoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = models.Admin.objects.filter(username = data['username']).first()
        if user is None:
            return Response({"result" : "User not found"})
        
        if user.password != data['password']:
            return Response({"result" : "Password Incorect"})


        return Response({"result" : "Success"})

class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = serializer.CategorySerializer
    queryset = models.Category.objects.all()

    def list(self, request, *args, **kwargs):

        child = self.get_child(0)
        res = {"result": child}

        return Response(res)

    def get_child(self, ids: int):
        result = {}
        q = models.Category.objects.filter(parent_category=ids).all()
        res = []
        if len(q) == 0:
            return res
        for i in q:
            child = self.get_child(i.id)
            result = {"category": i.name_category, "child": child, "id": i.id}
            res.append(result)
        return res
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data = {**data, "child" : self.get_child(data['id'])}
        return Response(data)


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
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "stock", "price"]
    search_fields = ["name"]
    ordering_fields = ("price",)
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        images = request.data.pop("images", [])

        data = {"images": images, "product": request.data}
        
        promo = request.data.get("promo", None)
        if not promo:
            no_promo = models.Promo.objects.get_or_create(promo_name = "No promo", promo_desc = "No Promo in this promo")
            data['product']["promo"] = no_promo[0].id
        serial = self.get_serializer(data=data)
        serial.is_valid(raise_exception=True)

        input_prod = {**serial.data["product"]}
        
        cat = models.Category.objects.get(id=int(input_prod["category"]))
        input_prod["category"] = cat

        promos = input_prod.pop("promo")

        product = models.Product.objects.create(**input_prod)
        product.save()

        for promo in promos:
            prom = models.Promo.objects.get_or_create(id=int(promo))
            product.promo.add(prom[0])

        product.save()

        res_img = []
        for image in images:
            img = models.Image.objects.create(image=image, product_id=product)
            res_img.append(img.__str__())
            img.save()

        data["images"] = res_img
        data["product"]["id"] = product.id

        return Response(data)

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.serializer_class["default"])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = []
            for item in serializer.data:
                item["images"] = self.get_url_image(item["id"])
                res.append(item)
            return self.get_paginated_response(res)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        ids = self.kwargs["pk"]
        data = serializer.ProductSerializer(self.get_object())

        images = self.get_url_image(ids)

        res = {**data.data, "images": images}

        return Response(res)

    def get_url_image(self, ids: str):
        images = models.Image.objects.filter(product_id=ids).all()
        res = [image.image.url for image in images]
        return res

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        data = serializer.data

        if "images" in request.data.keys():
            models.Image.objects.filter(product_id=obj.id).delete()
            img = request.data.pop("images", [])
            if img is not None:
                for i in img:
                    img = models.Image.objects.create(image=i, product_id=obj)
                    img.save()
                data["images"] = self.get_url_image(obj.id)

        return Response(data)


class AdBannerViewset(viewsets.ModelViewSet):
    queryset = models.AdBanner.objects.all()
    serializer_class = serializer.AdBannerSerializer


class EventViewset(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializer.EventSerializer
