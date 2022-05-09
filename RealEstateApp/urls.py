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
    path('detailproperty/<slug:slug>',
         views.PropertyDetailView.as_view(), name="detail_property"),
    path('mostviewed/', views.MosetViewdProperty.as_view(),
         name="most_viewed_property"),
    path('mostviewedproperties/', views.MosetViewdProperties.as_view(),
         name="most_viewed_properties"),
    path('createfeedback/<slug:slug>',
         views.CreateFeedbackView.as_view(), name="create_feedback")

]
