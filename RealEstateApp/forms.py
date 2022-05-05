from django import forms
from .models import Property, Address, Room
from django.forms import modelformset_factory
from django.forms.formsets import formset_factory


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_name', 'room_type', 'bed_room', 'beds', 'bed_type', 'guest', 'Address',
                  'cost', 'property_status', 'contact_number', 'cancellation', 'Description']
