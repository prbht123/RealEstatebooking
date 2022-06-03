from django.urls import path, include
from . import views

app_name = 'booking'
urlpatterns = [
    path('create/<slug:slug>', views.createBooking.as_view(), name='create_booking'),
    path('update/<slug:slug>/',
         views.bookingUpdateView.as_view(), name='Update_booking'),
    path('delete/<slug:slug>',
         views.bookingDeleteView.as_view(), name='delete_booking'),
    path('search/',
         views.SearchBookingView, name='booking_search'),
    path('why_us/', views.why_us, name='why_us'),
    path('contact/', views.ContactUpload, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('testing/', views.checking_hotel),
    path('sign/',views.sign_in),
]
