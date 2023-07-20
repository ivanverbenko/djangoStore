from django.contrib import admin

# Register your models here.
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = ('id', ('first_name', 'last_name'), ('email', 'adress'), 'basket_history', 'initiator')
    readonly_fields = ('id', 'created')
