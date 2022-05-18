from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import path, include, re_path
#from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/sign.html'), name="signin"),
    path('logout/', LogoutView.as_view(template_name='registration/signout.html'), name="logout"),
    path('register/', views.register, name='register'),
    path('profile/', views.homeView, name='home_profile'),
    path('userprofile/<int:pk>',
         views.UserProfileView, name="user_profile"),
    path('createuserprofile/', views.CreateUserProfileView.as_view(),
         name="create_user_profile"),
    path('edituserprofile/<slug:slug>', views.UpdateProfileView.as_view(),
         name='update_user_profile'),
    path('deleteuser/<slug:slug>', views.UserDeleteView, name='delete_user'),
]
