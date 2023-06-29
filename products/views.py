from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from products.models import Product, ProductCategory, Basket


def index(request):
    context={'title':'store'}
    return render(request, 'products/index.html',context=context)

def products(request):
    context = {'title': 'store-catalog',
               'products': Product.objects.all(),
               'categories': ProductCategory.objects.all()}
    return render(request, 'products/products.html',context)

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