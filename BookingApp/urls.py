from django.urls import path, include
from . import views
from .views import detail_view


app_name = 'booking'
urlpatterns = [
    path("create/",views.create_view),
    path("list_view/",views.list_view, name ='list_view'),
    path('<id>',views.detail_view ),
    

    ]


    