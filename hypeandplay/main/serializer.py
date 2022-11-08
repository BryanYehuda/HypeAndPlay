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
    images = serializers.RelatedField(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = "__all__"
        depth = 0
        
class ProductImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child = serializers.ImageField(use_url = True),
        required=False
    )
    product = ProductSerializer()
    
class AdBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdBanner
        fields = "__all__"
    