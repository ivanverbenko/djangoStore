from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from common.views import CommonMixin
from products.models import Basket, Product, ProductCategory


class IndexView(CommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = "Store"


class ProductsListView(CommonMixin, ListView):
    model = Product
    paginate_by = 6
    template_name = 'products/products.html'
    title = 'Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset().order_by('id')
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = cache.get('categories')
        if categories:
            context['categories'] = categories
        else:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        baskets.quantity += 1
        baskets.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
