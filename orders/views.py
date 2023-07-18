from http import HTTPStatus

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect


from common.views import CommonMixin
from orders.forms import OrderForm

import stripe

from store import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(CommonMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Спасибо за заказ'

class CancelTemplateView(CommonMixin, TemplateView):
    template_name = 'orders/cancel.html'


class OrderCreate(CommonMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Оформление заказа'
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreate, self).post(self, request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1NVLaJFZIPJsHLDcb3ub8bhe',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_cancel')),
        )
        return HttpResponseRedirect(checkout_session.url,status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreate, self).form_valid(form)