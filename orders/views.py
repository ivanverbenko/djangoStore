from django.views.generic.edit import CreateView
from orders.forms import OrderForm

class OrderCreate(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm