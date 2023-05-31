from django.shortcuts import render

# Create your views here.
from products.models import Product, ProductCategory


def index(request):
    context={'title':'store'}
    return render(request, 'products/index.html',context=context)

def products(request):
    context = {'title': 'store-catalog',
               'products': Product.objects.all(),
               'categories': ProductCategory.objects.all()}
    return render(request, 'products/products.html',context)