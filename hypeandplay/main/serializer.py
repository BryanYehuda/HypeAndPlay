from attr import fields
from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Category
        fields = "__all__"
        
class PromoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Promo
        fields = "__all__"
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        exclude = ("id",)
        depth = 0
        
class ProductImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child = serializers.ImageField()
    )
    product = ProductSerializer