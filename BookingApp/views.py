from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Booking, ContactDetails
from BookingApp.forms import BookingForm
from django.core.mail import send_mail
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
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
        return redirect('payment:process_stripe', slug=data.property.slug)


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


def why_us(request):
    """
        Why Us page Implementations.
    """
    return render(request, 'homepage/why_us.html')


# class ContactView(TemplateView):
#     template_name = 'homepage/contact.html'

def ContactUpload(request):
    if request.method == 'POST':
        obj = ContactDetails(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            mobile_number=request.POST.get('mobile'),
            messages=request.POST.get('message')
        )
        cd = {
            'to': 'saumyaranjan.webkrone@gmail.com'
        }
        msg = request.POST.get('message')
        send_mail("subject", msg, request.POST.get('email'), [cd['to']])
        messages.success(request, "Contact sent successfully")
        obj.save()
        return redirect('/homepage/contact/')
    else:
        print(settings.EMAIL_HOST_USER)
        return render(request, 'homepage/contact.html')
