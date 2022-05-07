from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createproperty/', views.CreateProperty.as_view(), name='create_property'),
    path('listproperty/', views.ListProperty.as_view(), name='list_property'),
    path('searchproperty/', views.SearchProperty.as_view(), name='search_property'),
    path('updateproperty/<slug:slug>/',
         views.PropertyUpdateView.as_view(), name='Update_property'),
    path('deleteproperty/<slug:slug>',
         views.PropertyDeleteView.as_view(), name='delete_property'),

]
