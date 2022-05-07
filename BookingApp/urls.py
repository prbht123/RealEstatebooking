from django.urls import path, include
from . import views


app_name = 'booking'
urlpatterns = [
    path("create/",views.create_view),
    path("list_view/",views.list_view, name ='list_view'),
    path('<id>/detail_view/',views.detail_view ),
    path('<id>/update/',views.update_view),
    path('<id>/delete/',views.delete_view ),

    ]


    