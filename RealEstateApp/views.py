from django.forms.models import inlineformset_factory
from telnetlib import DET
from django.shortcuts import render, redirect
from .models import Property, Address, Room
from BookingApp.models import Booking
from RealEstateApp.forms import PropertyForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
from django.db.models import Q
# Create your views here.


def home(request):
    return render(request, 'home.html')


class CreateProperty(CreateView):
    #model = Property
    form_class = PropertyForm
    template_name = 'property/create_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.save()
        return redirect('/')


class ListProperty(ListView):
    template_name = 'property/list_property.html'
    model = Property
    context_object_name = 'properties'


class SearchProperty(ListView):
    """
    Class view functon to handle search
    """
    template_name = 'property/search_property.html'
    model = Property
    #context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        city = self.request.GET.get('city')
        street = self.request.GET.get('street')
        country = self.request.GET.get('country')
        check_in_time = self.request.GET.get('checkintime')
        check_out_time = self.request.GET.get('checkouttime')
        context = super().get_context_data(**kwargs)
        if check_in_time and check_out_time:
            context['booking'] = Booking.objects.filter(
                Q(date_until__lt=check_in_time) | Q(date_from__gt=check_out_time))
            if context['booking']:
                context['booking'] = context['booking'].exclude(Q(date_from__lte=check_in_time, date_until__gte=check_in_time) | Q(
                    date_from__lte=check_out_time, date_until__gte=check_out_time))
            if context['booking']:
                context['booking'] = context['booking'].exclude(
                    date_from__lte=check_in_time, date_until__gte=check_out_time)
            if city and street and country:
                context['properties'] = context['booking'].filter(
                    property__Address__street=street, property__Address__city=city)
            else:
                context['properties'] = context['booking']
        elif city and street and country:
            context['propertiess'] = Property.objects.filter(
                Address__street=street, Address__city=city)
        else:
            context['propertiess'] = Property.objects.all()

        return context
