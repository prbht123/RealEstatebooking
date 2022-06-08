from django import views
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'payment'
urlpatterns = [
    path('process/<slug:slug>', views.payment_process, name='process'),
    path('process/stripe/<slug:slug>',
         views.PaymentWithStripe.as_view(), name='process_stripe'),
    path('stripe/done/<slug:slug>', views.payment_done_strip, name='stripe_done'),
    path('stripe/create/<slug:slug>', views.charge, name="stripe_payment_create"),
    path('done/<slug:slug>', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('api/checkout-session/<slug>/',
         views.create_checkout_session, name='api_checkout_session')
]
