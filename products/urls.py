from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products.views import *
app_name='products'
urlpatterns = [
    path('',products,name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)