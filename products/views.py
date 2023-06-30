from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator

def index(request):
    context={'title':'store'}
    return render(request, 'products/index.html',context=context)

def products(request, category_id=None, page_number=1):
    if category_id:
        products=Product.objects.filter(category__id=category_id)
    else:
        products=Product.objects.all()

    paginator = Paginator(products, 6)
    products_paginator = paginator.page(page_number)


    context = {'title': 'store-catalog',
               'products': products_paginator,
               'categories': ProductCategory.objects.all()}
    return render(request, 'products/products.html',context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product,quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def basket_remove(request, basket_id):
    basket=Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])