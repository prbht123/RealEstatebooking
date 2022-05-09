from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from BookingApp.forms import BookingForm

# Create your views here.


class CreateBooking(CreateView):
    #model = Property
    form_class = BookingForm
    template_name = 'booking/create_booking.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.paid = False
        data.save()
        print(data)
        print(data)
        print(data.property)
        print(data.property.slug)
        return redirect('payment:process', slug=data.property.slug)
