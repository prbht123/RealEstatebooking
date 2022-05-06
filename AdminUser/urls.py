from . import views
from django.urls import path, include, re_path
#from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('', views.AdminHome, name="admin_home"),
    path('manageuser', views.AdminManageUsers, name="manage_users"),
]
