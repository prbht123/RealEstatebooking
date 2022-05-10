from django import forms
from django.contrib.auth.models import User
from .models import AdminUserRoles


class AdminUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class AdminUserRolesForm(forms.ModelForm):
    class Meta:
        model = AdminUserRoles
        fields = ['roles']
