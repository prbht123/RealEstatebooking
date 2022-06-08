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
from RealEstateApp.models import Address, Property
from datetime import date
import datetime
import requests
# Create your views here.


class createBooking(CreateView):
    """
        Functionality for booking to the property.
    """
    form_class = BookingForm
    template_name = 'booking/create_booking.html'

    def form_valid(self, form):
        property = Property.objects.get(slug=self.kwargs['slug'])
        street = self.request.POST['street']
        city = self.request.POST['city']
        state = self.request.POST['state']
        country = self.request.POST['country']
        zip_code = self.request.POST['zip_code']
        checkin = self.request.POST['date_from']
        checkout = self.request.POST['date_until']
        checkin = datetime.datetime.strptime(checkin, '%Y-%m-%d %H:%M:%S')
        checkout = datetime.datetime.strptime(checkout, '%Y-%m-%d %H:%M:%S')
        day = checkout.date() - checkin.date()
        address = Address.objects.create(
            street=street, city=city, state=state, country=country, zip_code=zip_code)
        address.save()
        data = form.save(commit=False)
        data.address = address
        data.property = property
        data.paid = False
        if int(day.days) >= 1:
            data.cost = (int(day.days))*property.cost
        data.save()
        return redirect('payment:process', slug=data.slug)


class bookingUpdateView(UpdateView):
    """
        This class is used for updating of a particular property.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'booking/update_booking.html'
    success_url = '/home/'

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
    success_url = '/home/'


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
            'to': 'prabhat.webkrone@gmail.com'
        }
        msg = request.POST.get('message')
        send_mail("subject", msg, request.POST.get('email'), [cd['to']])
        messages.success(request, "Contact sent successfully")
        obj.save()
        return redirect('/booking/contact/')
    else:
        return render(request, 'home/contact.html')


def faq(request):
    """
        FAQ page implementation.
    """
    return render(request, 'homepage/faq.html')


def SearchBookingView(request):
    check_in_time = request.GET.get('checkin')
    check_in_time = datetime.datetime.strptime(
        check_in_time, "%Y-%m-%d").date()
    check_out_time = request.GET.get('checkout')
    check_out_time = datetime.datetime.strptime(
        check_out_time, "%Y-%m-%d").date()
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


def checking_hotel(request):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/reviews"

    querystring = {"hotel_id": "1676161", "locale": "en-gb", "sort_type": "SORT_MOST_RELEVANT",
                   "customer_type": "solo_traveller,review_category_group_of_friends", "language_filter": "en-gb,de,fr"}
    headers = {
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
        "X-RapidAPI-Key": "a284490392msh8bc2f4fca36314bp174298jsnf2e183c30573"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    print(response.text[0][0])
    return render(request, 'bookingtest.html', {'context': response})
