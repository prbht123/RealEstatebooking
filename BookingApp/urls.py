from django.urls import path, include
from . import views

app_name = 'booking'
urlpatterns = [
    path('create/', views.createBooking.as_view(), name='create_booking'),
    path('update/<slug:slug>/',
         views.bookingUpdateView.as_view(), name='Update_booking'),
]
