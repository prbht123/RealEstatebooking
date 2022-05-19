from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Booking, ContactDetails
from BookingApp.forms import BookingForm
from django.core.mail import send_mail
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.views.generic import TemplateView
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from django.http import JsonResponse
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
        return redirect('payment:process_stripe', slug=data.slug)


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


def faq(request):
    """
        FAQ page implementation.
    """
    return render(request, 'homepage/faq.html')


def SearchBookingView(request):
    check_in_time = request.GET.get('checkin')
    check_in_time = datetime.strptime(check_in_time, "%Y-%m-%d").date()
    check_out_time = request.GET.get('checkout')
    check_out_time = datetime.strptime(check_out_time, "%Y-%m-%d").date()
    property_slug = request.GET.get('property_slug')
    context = {}
    if check_in_time and check_out_time:
        context['booking'] = Booking.objects.filter(
            Q(date_until__lt=check_in_time) | Q(date_from__gt=check_out_time))
        if not context['booking']:
            context['booking'] = Booking.objects.all().exclude(Q(date_from__lte=check_in_time, date_until__gte=check_in_time) | Q(
                date_from__lte=check_out_time, date_until__gte=check_out_time))
            if not context['booking']:
                context['booking'] = Booking.objects.filter(
                    date_from__lte=check_in_time, date_until__gte=check_out_time)

    if context['booking']:
        context['booking'] = context['booking'].filter(
            property__slug=property_slug)
        return JsonResponse({'status': 1})
    return JsonResponse({'status': 0})
