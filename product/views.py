from django.shortcuts import render
from .models import Products
from .filters import ProductFilter
from .models import Category, Store

def home(request):
    product_list = Products.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    categories = Category.objects.all()
    store = Store.objects.all()
    context = {
        'filter': product_filter,
    }
    return render(request, 'products/home.html', context)

