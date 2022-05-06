from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import path, include, re_path
#from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/sign.html'), name="signin"),
    path('logout/', LogoutView.as_view(template_name='registration/signout.html'), name="logout"),
    path('register/', views.register, name='register'),

]
