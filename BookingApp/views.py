from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking,Address,Contact
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Booking
from BookingApp.forms import BookingForm
from django.core.mail import send_mail


# def create_view(request):
   
#     context ={}
 
#     # add the dictionary during initialization
#     form = BookingForm(request.POST )
#     if form.is_valid():
#         form.save()
#     context['form']= form
#     return render(request, "create_booking.html",context)


# def list_view(request):
#     context ={}
#     # add the dictionary during initialization
#     context['dataset'] = Booking.objects.all()
    
#     return render(request, "list_view.html", context)

# def detail_view(request, id):
   
#     context ={}
#     print("000000000000000000000000")
#     context["data"] = Booking.objects.get(id = id)
#     print(context["data"])
#     return render(request, "detail_view.html", context)


# def update_view(request, id):
#     context ={}
#     obj = get_object_or_404(Booking, id = id)
#     if request.method == 'POST':
#         form = BookingForm(request.POST or None, instance = obj)
#         #form = BookingForm(request.POST, instance = obj )
#         print(form.is_valid())
#         if form.is_valid():
#             form.save()
#             return redirect('list_view')
#             context["form"] = form
#     else:
#         form = BookingForm()
#         context["form"] = form
#     return render(request, "update_view.html", context)





# def delete_view(request, id):
    
#     context ={}
#     obj = get_object_or_404(Booking, id = id)
 
#     if request.method =="POST":
#         obj.delete()
#         return HttpResponseRedirect("/")
 
#     return render(request, "delete_view.html", context)


def homepage(request):
    return render(request, 'bookingpage/home1.html')

def why_us(request):
    return render(request, 'bookingpage/why_us.html')

class ContactView(TemplateView):
    template_name = 'bookingpage/contact.html'
    def ContactUpload(request):
        if request.method == 'POST':
            obj = ContactDetail(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            mobile_number = request.POST.get('mobile'),
            messages = request.POST.get('message')
            )
            obj.save()
            cd={
            'to':'saumyaranjan.webkrone@gmail.com'
            }
            print("111111111111111111")
            msg=request.POST.get('message')
            send_mail("subject",msg,request.POST.get('email'),[cd['to']])
            messages.success(request,"Contact sent successfully")
            return redirect('/bookingpage/contact/')


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
    model = Booking
    template_name = 'booking/delete_booking.html'
    success_url = '/'


def faq(request):
    return render(request, 'bookingpage/faq.html')

