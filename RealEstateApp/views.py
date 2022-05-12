from django.forms.models import inlineformset_factory
from telnetlib import DET
from django.shortcuts import render, redirect
from .models import FeedBackProperty, Property, Address, RankingProperty, Room, MostViewed
from BookingApp.models import Booking
from RealEstateApp.forms import FeedbackForm, PropertyForm, RankingPropertyForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
from django.db.models import Q
from django.urls import reverse
from django.db.models import Avg
# Create your views here.


def home(request):
    return render(request, 'bookingpage/home1.html')
    context = {}
    context['properties'] = MostViewed.objects.all().order_by('-viewed')[:4]
    return render(request, 'home.html', context)



class createProperty(CreateView):
    """
        Creted property functionality.
    """
    model = Property
    form_class = PropertyForm
    template_name = 'property/create_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.author = self.request.user
        data.image = self.request.FILES['myFile']
        data.save()
        count = MostViewed.objects.create(property=data, viewed=0)
        count.save()
        return redirect('/')


class listProperty(ListView):
    """
        List out the all properties.
    """
    template_name = 'property/list_property.html'
    model = Property
    context_object_name = 'properties'


class searchProperty(ListView):
    """
    Class view functon to handle search as location,check-in and check-out wise.
    """
    template_name = 'property/search_property.html'
    model = Property
    # context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        city = self.request.GET.get('city')
        street = self.request.GET.get('street')
        country = self.request.GET.get('country')
        check_in_time = self.request.GET.get('checkintime')
        check_out_time = self.request.GET.get('checkouttime')
        context = super().get_context_data(**kwargs)
        if check_in_time and check_out_time:
            context['booking'] = Booking.objects.filter(
                Q(date_until__lt=check_in_time) | Q(date_from__gt=check_out_time))
            if not context['booking']:
                context['booking'] = Booking.objects.all().exclude(Q(date_from__lte=check_in_time, date_until__gte=check_in_time) | Q(
                    date_from__lte=check_out_time, date_until__gte=check_out_time))
                if not context['booking']:
                    context['booking'] = Booking.objects.filter(
                        date_from__lte=check_in_time, date_until__gte=check_out_time)

            if city and street:
                context['propertiess'] = Property.objects.filter(
                    Address__street=street, Address__city=city)
                if context['booking']:
                    for book in context['booking']:
                        context['propertiess'] = context['propertiess'].exclude(
                            slug=book.property.slug)
            else:
                context['properties'] = context['booking']
        elif city and street:
            context['propertiess'] = Property.objects.filter(
                Address__city=city, Address__street=street)
        else:
            context['propertiess'] = Property.objects.all()

        return context


class propertyUpdateView(UpdateView):
    """
        This class is used for updating of a particular property.
    """
    model = Property
    form_class = PropertyForm
    template_name = 'property/property_update.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(propertyUpdateView, self).get_form_kwargs()
        kwargs.update()
        return kwargs


class propertyDeleteView(DeleteView):
    """
        Delete view function for particular property.
    """
    model = Property
    template_name = 'property/property_delete.html'
    success_url = '/'


class propertyDetailView(DetailView):
    """
        This class is used for showing a particular property's detail.
    """
    model = Property
    template_name = 'property/property_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property'] = Property.objects.filter(slug=self.object.slug)[0]
        context['ranking'] = RankingProperty.objects.filter(
            property__slug=self.object.slug).aggregate(Avg('rank'))
        context['feedback'] = FeedBackProperty.objects.filter(
            property__slug=self.object.slug)
        count = MostViewed.objects.get(
            property__slug=context['property'].slug)
        count.viewed = count.viewed + 1
        count.save()
        return context


class mosetViewedProperty(ListView):
    """
        Top 5 Mostviewed property functionality.
    """
    template_name = 'property/most_viewed_property.html'
    model = Property
    context_object_name = 'properties'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = MostViewed.objects.all().order_by('-viewed')[:5]
        print(context['properties'])
        return context


class mosetViewedProperties(ListView):
    """
        List out the all properties as mostviewed. 
    """
    template_name = 'property/most_viewed_all_properties.html'
    model = Property
    context_object_name = 'properties'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = MostViewed.objects.all().order_by('-viewed')
        print(context['properties'])
        return context


class createFeedbackView(CreateView):
    """
        Created feedback for a particular property.
    """
    model = FeedBackProperty
    form_class = FeedbackForm
    template_name = 'feedback/create_feedback_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        property = Property.objects.get(slug=self.kwargs['slug'])
        data.property = property
        data.save()
        return redirect('/')


class createRankingView(CreateView):
    """
        Give the ranck to a property.
    """
    model = RankingProperty
    form_class = RankingPropertyForm
    template_name = 'ranking/create_ranking_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        print(self.kwargs['slug'])
        property = RankingProperty.objects.filter(
            user=self.request.user, property__slug=self.kwargs['slug'])
        if not property:
            if data.rank > 5:
                return redirect('create_ranking_property', slug=self.kwargs['slug'])
            data.user = self.request.user
            property = Property.objects.get(slug=self.kwargs['slug'])
            data.property = property
            data.save()

        return redirect('/')


class propertyNameSearchView(ListView):
    """
        Property wise search bar functionality.
    """
    template_name = 'property/search_with_property_name.html'
    model = Property

    def get_context_data(self, **kwargs):
        property = self.request.GET.get('property')
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.filter(
            property_name__icontains=property)
        return context


class imagesRecentPropertiesSliderView(ListView):
    """
        Get images from recent added properties functionality.
    """
    template_name = 'property/list_property.html'
    model = Property

    def get_context_data(self, **kwargs):
        property = self.request.GET.get('property')
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.all().order_by(
            '-created_date')[:8]
        print(context['properties'])
        return context
