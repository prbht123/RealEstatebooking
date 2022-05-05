from django.forms.models import inlineformset_factory
from telnetlib import DET
from django.shortcuts import render, redirect
from .models import Property, Address, Room
from RealEstateApp.forms import PropertyForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
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
