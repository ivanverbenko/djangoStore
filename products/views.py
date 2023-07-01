from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView, CreateView

from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Store'
        return context

class ProductsListView(ListView):
    model = Product
    paginate_by = 6
    template_name = 'products/products.html'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Catalog'
        context['categories'] = ProductCategory.objects.all()
        return context


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