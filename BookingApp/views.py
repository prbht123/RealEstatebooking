from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import BookingForm
from .models import Booking,Address,Contact
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from django.views.generic import TemplateView
 



def create_view(request):
   
    context ={}
 
    # add the dictionary during initialization
    form = BookingForm(request.POST )
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request, "create_booking.html",context)


def list_view(request):
    context ={}
    # add the dictionary during initialization
    context['dataset'] = Booking.objects.all()
    
    return render(request, "list_view.html", context)

def detail_view(request, id):
   
    context ={}
    print("000000000000000000000000")
    context["data"] = Booking.objects.get(id = id)
    print(context["data"])
    return render(request, "detail_view.html", context)


def update_view(request, id):
    context ={}
    obj = get_object_or_404(Booking, id = id)
    if request.method == 'POST':
        form = BookingForm(request.POST or None, instance = obj)
        #form = BookingForm(request.POST, instance = obj )
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('list_view')
            context["form"] = form
    else:
        form = BookingForm()
        context["form"] = form
    return render(request, "update_view.html", context)





def delete_view(request, id):
    
    context ={}
    obj = get_object_or_404(Booking, id = id)
 
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/")
 
    return render(request, "delete_view.html", context)


def homepage(request):
    return render(request, 'bookingpage/home1.html')

class Contact(TemplateView):
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
            'to':'Admin123@YOPmail.com'
            }
            msg=request.POST.get('message')
            send_mail("subject",msg,request.POST.get('email'),[cd['to']])
            messages.success(request,"Contact sent successfully")
            return redirect('/bookingpage/contact/')












 


