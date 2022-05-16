from django.urls import path, include
from . import views

app_name = 'booking'
urlpatterns = [
    path('create/', views.createBooking.as_view(), name='create_booking'),
    path('update/<slug:slug>/',
         views.bookingUpdateView.as_view(), name='Update_booking'),
    path('delete/<slug:slug>',
         views.bookingDeleteView.as_view(), name='delete_booking'),
    path('why_us/', views.why_us, name='why_us'),
    path('contact/', views.ContactUpload),
    path('faq/', views.faq),
]
