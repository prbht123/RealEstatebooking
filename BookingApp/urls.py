from django.urls import path, include
from . import views

app_name = 'booking'
urlpatterns = [
    path('create/', views.CreateBooking.as_view(), name='create_booking'),
]
