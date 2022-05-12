from django.urls import path, include
from .import views


app_name = 'booking'
urlpatterns = [

    path("create/",views.create_view),
    path("list_view/",views.list_view, name ='list_view'),
    path('detail/<int:id>/',views.detail_view ),
    path('update/<int:id>/',views.update_view ),
    path('delete/<int:id>/',views.delete_view ),
    path('home1/', views.homepage),
    path('why_us/',views.why_us),
    path('contact/',views.ContactView.as_view()),

    
    path('create/', views.createBooking.as_view(), name='create_booking'),
    path('update/<slug:slug>/',
         views.bookingUpdateView.as_view(), name='Update_booking'),
    path('delete/<slug:slug>',
         views.bookingDeleteView.as_view(), name='delete_booking'),
]

