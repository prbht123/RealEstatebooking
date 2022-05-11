from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Booking
from BookingApp.forms import BookingForm

# Create your views here.


class createBooking(CreateView):
    """
        Functionality for booking to the property.
    """
    form_class = BookingForm
    template_name = 'booking/create_booking.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.paid = False
        data.save()
        return redirect('payment:process', slug=data.property.slug)


class bookingUpdateView(UpdateView):
    """
        This class is used for updating of a particular property.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'booking/update_booking.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(bookingUpdateView, self).get_form_kwargs()
        print(kwargs['instance'])
        kwargs.update()
        return kwargs


class bookingDeleteView(DeleteView):
    """
        Delete view function for particular booking.
    """
    model = Booking
    template_name = 'booking/delete_booking.html'
    success_url = '/'
