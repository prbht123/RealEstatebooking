from django import views
from django.urls import path, include
from django.conf import settings
from . import views
app_name = 'payment'
urlpatterns = [
    path('process/<slug:slug>', views.payment_process, name='process'),
    path('done/<slug:slug>', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
