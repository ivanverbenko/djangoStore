from http import HTTPStatus

from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponse

from common.views import CommonMixin
from orders.forms import OrderForm

import stripe

from products.models import Basket
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
        basket = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=basket.stripe_products(),
            metadata={'order_id':self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_cancel')),
        )
        return HttpResponseRedirect(checkout_session.url,status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreate, self).form_valid(form)

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )


        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    order_id = int(session.metadata.order_id)
    print("Fulfilling order")