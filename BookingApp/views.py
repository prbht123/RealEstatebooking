from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking,Address
# from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView





def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = BookingForm(request.POST )
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request, "create_booking.html",context)


def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    # add the dictionary during initialization
    context['dataset'] = Booking.objects.all()

    return render(request, "list_view.html", context)
















 


