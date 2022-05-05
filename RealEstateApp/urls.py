from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('createproperty/', views.CreateProperty.as_view(), name='create_property')
]
