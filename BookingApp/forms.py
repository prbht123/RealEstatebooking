from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    street = forms.CharField(label='Street', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    zip_code = forms.CharField(label='Zip Code', max_length=100)

    class Meta:
        model = Booking
        fields = ['gender', 'firstname', 'lastname', 'nationality', 'email', 'mobile_Number',
                  'date_from', 'date_until', 'street', 'city', 'state', 'country', 'zip_code', 'notes']
