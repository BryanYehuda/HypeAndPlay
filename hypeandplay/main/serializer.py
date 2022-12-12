from rest_framework import serializers
from . import models
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=models.User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'is_superuser', "groups")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data : dict):
        super_user = validated_data.pop('is_superuser', False)
        if super_user:
            staff = True
        else:
            staff = False
        groups = validated_data.pop('groups', [2])
        user = models.User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_superuser = super_user,
            is_staff = staff
        )
        
        user.set_password(validated_data['password'])
        user.save()
        g = Group.objects.all()
        for group in groups:
            user.groups.add(group)

        return user

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
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = "__all__"
        
class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = models.Cart
        fields = ("items", "total_items", "user")
        depth = 2