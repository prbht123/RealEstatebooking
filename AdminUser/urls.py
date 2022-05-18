from . import views
from django.urls import path, include, re_path
#from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('', views.adminHome, name="admin_home"),
    path('manageuser', views.adminManageUsers, name="manage_users"),
    path('register/', views.adminRegisterUser, name='admin_register_user'),
    path('delete/<int:pk>', views.deleteAdminUser,
         name="delete_admin_user"),
    path('createrole/<int:pk>', views.createRoleAdmin.as_view(), name='create_role'),
    path('manageuserrole/', views.adminManageUsersRoles.as_view(),
         name="manage_admin_role"),
    path('editrole/<slug:slug>', views.roleUpdateView.as_view(),
         name="edit_role_admin_user"),
    path('deleterole/<slug:slug>', views.deleteAdminUserRoles.as_view(),
         name="delete_role_admin_user"),
    path('normalusers/', views.listAllUsersView.as_view(), name='normal_users'),
    path('convertadmin/<int:pk>', views.convertNormalUserToAdmin,
         name='convert_admin_from_normal_user'),
    path('deleteuser/<int:pk>/', views.deleteUsersByAdminUsers.as_view(),
         name='delete_users_by_admin'),
    path('approvingpropertylist/', views.listAllPropertyView.as_view(),
         name='approving_property_list'),
    path('approvingproperty/<slug:slug>', views.approvedPropertyView,
         name='approved_property'),
    path('addpopularlocation', views.CreatePopularLocationView.as_view(),
         name="add_popular_location"),
]
