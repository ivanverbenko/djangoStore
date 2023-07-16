from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from common.views import CommonMixin
from orders.forms import OrderForm

class OrderCreate(CommonMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Оформление заказа'
    success_url = reverse_lazy('orders:order_create')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreate, self).form_valid(form)