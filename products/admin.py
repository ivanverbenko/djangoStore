from django.contrib import admin
from django.db.models.functions import Lower
# Register your models here.
from django.contrib import admin
from products.models import ProductCategory,Product, Basket

admin.site.register(ProductCategory)
#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = [field.name for field in Product._meta.fields if field.name != "id"]
    search_fields = ('name', 'price')
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product','quantity')
    extra = 0