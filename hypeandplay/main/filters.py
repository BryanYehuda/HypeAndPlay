from attr import fields
from django_filters import FilterSet, RangeFilter
from .models import Product

class ProductFilter(FilterSet):
    price = RangeFilter()
    
    class Meta:
        model = Product
        fields = ['price']