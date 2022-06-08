from django.shortcuts import redirect, render, get_object_or_404
from BookingApp.models import Booking
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
import stripe
from paypal.standard.forms import PayPalPaymentsForm
import json
from RealEstateApp.models import Property
from django.http import HttpResponse
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def payment_done(request, **kwargs):
    booked = Booking.objects.get(slug=kwargs['slug'])
    booked.paid = True
    booked.save()
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request, slug):
    #order_id = request.session.get('order_id')
    booked = get_object_or_404(Booking, slug=slug)
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % booked.cost,
        'item_name': 'Booked {}'.format(booked.id),
        'invoice': str(booked.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done', kwargs={'slug': booked.slug})),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': booked, 'form': form})

    # key = settings.STRIPE_PUBLISHABLE_KEY
    # return render(request, 'payment/stripe/process.html', {'order': booked, 'form': form, 'key': key})


class PaymentWithStripe(TemplateView):
    template_name = 'payment/stripe/process.html'

    def get_context_data(self, **kwargs):
        booked = get_object_or_404(Booking, slug=kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['booked'] = booked
        return context


def charge(request, slug):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount="90",
            currency="usd",
            description="payment by stripe",
            source=request.POST['stripeToken']
        )
    return render(request, 'payment/done.html', {'slug': slug})


@csrf_exempt
def create_checkout_session(request, slug):

    #request_data = json.loads(request.body)
    booked = get_object_or_404(Booking, slug=slug)
    product = get_object_or_404(Property, pk=booked.property.id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    CHECKOUT_SESSION_ID = "cs_test_a1gneAizS7gv1OVGYiIW51F4eqlpAFGwAV3Yill6CK7gXBw9mCjwDUU8Qt#fidkdWxOYHwnPyd1blpxYHZxWjA0Tnx3c2RWQFUwVktpVnRzS0BCbFYzaWh8YVdPV2xjXW80UmZtRHB3akJMYmRUc0BJc1FqYGFzdlx9SUBAPUhoZGhWbU5odFRAQ0xiZ25oQn9kd0NsZGltNTVtNUsxcTFOaycpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        #customer_email = request_data['email'],
        customer_email='developers.prabhat.webkrone@gmail.com',
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.property_name,
                    },
                    'unit_amount': int(product.cost * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment:stripe_done', kwargs={'slug': booked.slug})
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment:canceled')),
    )
    print(checkout_session)
    print("hello")
    return redirect("/home/")


def payment_done_strip(request, **kwargs):
    booked = Booking.objects.get(slug=kwargs['slug'])
    booked.paid = True
    booked.save()
    return render(request, 'payment/done.html')
