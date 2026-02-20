from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment-success', views.payment_success, name='payment-success'),
    path('payment-success', views.payment_success, name='payment-success'),
    path('checkout', views.checkout, name='checkout'),

]