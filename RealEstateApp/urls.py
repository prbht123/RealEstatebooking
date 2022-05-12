from django.urls import path, include
from . import views

urlpatterns = [

    path('home/', views.home, name='home'),
    path('createproperty/', views.createProperty.as_view(), name='create_property'),
    path('listproperty/', views.listProperty.as_view(), name='list_property'),
    path('searchproperty/', views.searchProperty.as_view(), name='search_property'),
    path('', views.home, name='home'),
    path('createproperty/', views.createProperty.as_view(), name='create_property'),
    path('listproperty/', views.listProperty.as_view(), name='list_property'),
    path('searchproperty/', views.searchProperty.as_view(), name='search_property'),
    path('updateproperty/<slug:slug>/',
         views.propertyUpdateView.as_view(), name='Update_property'),
    path('deleteproperty/<slug:slug>',
         views.propertyDeleteView.as_view(), name='delete_property'),
    path('detailproperty/<slug:slug>',
         views.propertyDetailView.as_view(), name="detail_property"),
    path('mostviewed/', views.mosetViewedProperty.as_view(),
         name="most_viewed_property"),
    path('mostviewedproperties/', views.mosetViewedProperties.as_view(),
         name="most_viewed_properties"),
    path('createfeedback/<slug:slug>',
         views.createFeedbackView.as_view(), name="create_feedback_property"),
    path('createranking/<slug:slug>',
         views.createRankingView.as_view(), name="create_ranking_property"),
    #  path('listrankfeedbackproperty/<slug:slug>',
    #      views.ListRankFeedbackProperty.as_view(), name="list_rank_feedback_property")
    path('searchpropertyname/', views.propertyNameSearchView.as_view(),
         name='search_with_property_name'),
    path('imagesrecentproperty/', views.imagesRecentPropertiesSliderView.as_view(),
         name='images_recent_property'),
]
