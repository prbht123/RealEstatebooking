from django.shortcuts import render, get_object_or_404
from BookingApp.models import Booking
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request, slug):
    #order_id = request.session.get('order_id')
    booked = get_object_or_404(Booking, property__slug=slug)
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % booked.cost,
        'item_name': 'Booked {}'.format(booked.id),
        'invoice': str(booked.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    booked.paid = True
    booked.save()
    return render(request, 'payment/process.html', {'order': booked, 'form': form})
