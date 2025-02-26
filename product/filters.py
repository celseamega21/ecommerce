import django_filters
from .models import Products

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    store = django_filters.CharFilter(field_name='store__name', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    subcategory = django_filters.CharFilter(field_name='subcategory__subcategory', lookup_expr='icontains')
    
    class Meta:
        model = Products
        fields = ['name', 'store', 'min_price', 'max_price', 'category', 'subcategory']
