from django.contrib import admin

# Register your models here.
from django.contrib import admin
from products.models import ProductCategory,Product

admin.site.register(ProductCategory)
admin.site.register(Product)