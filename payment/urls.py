from django import views
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'payment'
urlpatterns = [
    path('process/<slug:slug>', views.payment_process, name='process'),
    path('process/stripe/<slug:slug>',
         views.PaymentWithStripe.as_view(), name='process_stripe'),
    path('stripe/done', views.payment_done_strip, name='stripe_done'),
    path('done/<slug:slug>', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
