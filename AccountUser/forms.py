from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserProfileForm(forms.ModelForm):
    street = forms.CharField(label='street', max_length=100)
    city = forms.CharField(label='city', max_length=100)
    state = forms.CharField(label='state', max_length=100)
    country = forms.CharField(label='country', max_length=100)
    zip_code = forms.CharField(label='zip_code', max_length=100)
    first_name = forms.CharField(label='first_name', max_length=100)
    last_name = forms.CharField(label='last_name', max_length=100)

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','contact_number', 'street',
                  'city', 'state', 'country', 'zip_code']
