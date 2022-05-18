from django import forms
from django.contrib.auth.models import User
from .models import AdminUserRoles, PopularLocations


class AdminUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class AdminUserRolesForm(forms.ModelForm):
    class Meta:
        model = AdminUserRoles
        fields = ['roles']


class PopularLocationsForms(forms.ModelForm):
    class Meta:
        model = PopularLocations
        fields = ['city', 'state', 'country', 'popular_rank']
