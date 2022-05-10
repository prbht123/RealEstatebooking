from . import views
from django.urls import path, include, re_path
#from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('', views.AdminHome, name="admin_home"),
    path('manageuser', views.AdminManageUsers, name="manage_users"),
    path('register/', views.AdminRegisterUser, name='admin_register_user'),
    path('delete/<int:pk>', views.DeleteAdminUser,
         name="delete_admin_user"),
    path('createrole/<int:pk>', views.CreateRoleAdmin.as_view(), name='create_role'),
    path('manageuserrole/', views.AdminManageUsersRoles.as_view(),
         name="manage_admin_role"),
    path('editrole/<slug:slug>', views.RoleUpdateView.as_view(),
         name="edit_role_admin_user"),
    path('deleterole/<slug:slug>', views.DeleteAdminUserRoles.as_view(),
         name="delete_role_admin_user")
]
