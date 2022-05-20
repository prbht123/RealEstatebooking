from django import forms
from .models import Property, Address, Room, FeedBackProperty, RankingProperty
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory
#from django_countries.fields import CountryField
#from django_countries.widgets import CountrySelectWidget


class PropertyForm(forms.ModelForm):
    street = forms.CharField(label='Street', max_length=100)
    city = forms.CharField(label='City', max_length=100)
    state = forms.CharField(label='State', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    zip_code = forms.CharField(label='Zip Code', max_length=100)
    room_type1 = forms.CharField(label='Room Type', max_length=100)

    class Meta:
        model = Property
        fields = ['property_name', 'room_type1', 'bed_room', 'beds', 'bed_type', 'guest',
                  'cost', 'contact_number', 'Description', 'cancellation', 'street', 'city', 'state', 'country', 'zip_code']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBackProperty
        fields = ['feedback']


class RankingPropertyForm(forms.ModelForm):
    class Meta:
        model = RankingProperty
        fields = ['rank']
