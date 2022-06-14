from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
# from django.urls import include, url

app_name = "account"
urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/signinnew.html'), name="signin"),
    path('logout/', LogoutView.as_view(template_name='registration/signout.html'), name="logout"),
    path('register/', views.register, name='register'),
    path('profile/<int:pk>', views.UserProfileDetailView.as_view(),
         name='user_profile_view'),
    path('passwordchange/', PasswordChangeView.as_view(
        template_name='registration/password_change_form.html', success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    path('passwordchange/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'), name='password_change_done'),
    path('userprofile/<int:pk>',
         views.UserProfileView, name="user_profile"),
    path('createuserprofile/', views.CreateUserProfileView.as_view(),
         name="create_user_profile"),
    path('edituserprofile/<slug:slug>', views.UpdateProfileView.as_view(),
         name='update_user_profile'),
    path('deleteuser/<slug:slug>', views.UserDeleteView, name='delete_user'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',
         subject_template_name='registration/password_reset_subject.txt', email_template_name='registration/password_reset_email.html', success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

]
