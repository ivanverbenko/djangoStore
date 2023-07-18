from django.urls import path

from orders.views import OrderCreate, SuccessTemplateView,CancelTemplateView

app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('order-success',SuccessTemplateView.as_view(), name='order_success'),
    path('order-cancel', CancelTemplateView.as_view(), name='order_cancel')
]