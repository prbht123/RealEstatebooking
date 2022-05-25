from tkinter import Image
from django.forms.models import inlineformset_factory
from telnetlib import DET
from django.http import JsonResponse
from django.shortcuts import render, redirect

from AdminUser.models import PopularLocations
from .models import FeedBackProperty, Property, Address, RankingProperty, Room, MostViewed, ImagesProperty, Room
from BookingApp.models import Booking
from RealEstateApp.forms import FeedbackForm, PropertyForm, RankingPropertyForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
from django.db.models import Q
from django.urls import reverse
from django.db.models import Avg, Count
import json
from AccountUser.models import UserProfile
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.


def home(request):
    context = {}
    context['propertiess'] = Property.objects.all()
    context['properties'] = MostViewed.objects.filter(
        property__property_status='published').order_by('-viewed')[:4]
    context['ranking'] = RankingProperty.objects.filter(property__property_status='published').values(
        'property').annotate(avg=Avg('rank')).order_by('-avg')
    context['propertiesr'] = []
    for item in context['ranking']:
        data = Property.objects.get(id=item['property'])
        context['propertiesr'].append(data)
    popular_locations = PopularLocations.objects.all()
    context['popular_location_property'] = []
    context['famousproperty'] = Property.objects.filter(property_status='published').values(
        'Address__city').annotate(count=Count('property_name')).order_by('-count')
    print(context['famousproperty'])
    context['famoupropertylist'] = []
    for famous in context['famousproperty']:
        property = Property.objects.filter(
            property_status='published', Address__city=famous['Address__city'])[0]
        data = {
            'Address_city': famous['Address__city'],
            'count': famous['count'],
            'property': property,
        }
        context['famoupropertylist'].append(data)
    print(context['famoupropertylist'])
    for popular in popular_locations:
        city = (popular.city).lower()
        state = (popular.state).lower()
        ranking_property = RankingProperty.objects.filter(
            property__property_status='published', property__Address__city=city, property__Address__state=state, property__Address__country=popular.country)
        if ranking_property:
            popular_location_property = ranking_property.values(
                'property').annotate(avg=Avg('rank')).order_by('-avg')[0]
            data = Property.objects.get(
                id=popular_location_property['property'])
            context['popular_location_property'].append(data)

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
        street = self.request.POST['street']
        city = self.request.POST['city']
        state = self.request.POST['state']
        country = self.request.POST['country']
        zip_code = self.request.POST['zip_code']
        room_type = self.request.POST['room_type1']
        room = Room.objects.create(room_type_name=room_type)
        room.save()
        address = Address.objects.create(
            street=street, city=city, state=state, country=country, zip_code=zip_code)
        address.save()
        data.Address = address
        data.room_type = room
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
    paginate_by = 5
    #context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['propertiess'] = Property.objects.filter(
            property_status='published')
        context['properties'] = []
        for property in context['propertiess']:
            rank = RankingProperty.objects.filter(
                property=property).aggregate(avg=Avg('rank'))
            viewed = MostViewed.objects.get(property=property)
            if rank['avg'] is not None:
                rank = "{:.2f}".format(rank['avg'])
            else:
                rank = 0
            data = {
                'property': property,
                'rank': rank,
                'viewed': viewed.viewed,
            }
            context['properties'].append(data)
        paginator = Paginator(context['properties'], self.paginate_by)

        page = self.request.GET.get('page')

        try:
            property = paginator.page(page)
        except PageNotAnInteger:
            property = paginator.page(1)
        except EmptyPage:
            property = paginator.page(paginator.num_pages)
        context['properties'] = property
        return context


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
                    Address__street=street, Address__city=city, property_status='published')
                if context['booking']:
                    for book in context['booking']:
                        context['propertiess'] = context['propertiess'].exclude(
                            slug=book.property.slug)
            else:
                context['propertiess'] = Property.objects.filter(
                    property_status='published')
                for book in context['booking']:
                    context['propertiess'] = context['propertiess'].exclude(
                        slug=book.property.slug)
                #context['properties'] = context['booking']
        elif city and street:
            context['propertiess'] = Property.objects.filter(property_status='published',
                                                             Address__city=city, Address__street=street)
        else:
            context['propertiess'] = Property.objects.filter(
                property_status='published')
        context['properties'] = []
        for property in context['propertiess']:
            print(property)
            rank = RankingProperty.objects.filter(
                property=property).aggregate(avg=Avg('rank'))
            viewed = MostViewed.objects.filter(property=property)
            if rank['avg'] is not None:
                rank = "{:.2f}".format(rank['avg'])
            else:
                rank = 0
            data = {
                'property': property,
                'rank': rank,
                'viewed': viewed[0].viewed,
            }
            context['properties'].append(data)
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
        context['images'] = ImagesProperty.objects.filter(
            property__slug=self.object.slug)
        context['ranking'] = RankingProperty.objects.filter(
            property__slug=self.object.slug).aggregate(Avg('rank'))
        context['feedback'] = FeedBackProperty.objects.filter(
            property__slug=self.object.slug)
        context['booking'] = list(Booking.objects.filter(
            property__slug=self.object.slug))
        context['feedbackform'] = FeedbackForm
        context['form'] = RankingPropertyForm
        context['userprofiles'] = UserProfile.objects.all()
        count = MostViewed.objects.get(
            property__slug=context['property'].slug)
        if count.property.author == self.request.user:
            pass
        else:
            count.viewed = count.viewed + 1
            count.save()
        return context


class mostViewedProperty(ListView):
    """
        Top 5 Mostviewed property functionality.
    """
    template_name = 'property/most_viewed_property.html'
    model = Property
    context_object_name = 'properties'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = MostViewed.objects.filter(
            property__property_status='published').order_by('-viewed')[:5]
        print(context['properties'])
        return context


class mostViewedProperties(ListView):
    """
        List out the all properties as mostviewed. 
    """
    template_name = 'property/most_viewed_all_properties.html'
    model = Property
    context_object_name = 'properties'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['propertiess'] = MostViewed.objects.filter(
            property__property_status='published').order_by('-viewed')
        context['properties'] = []
        for property in context['propertiess']:
            rank = RankingProperty.objects.filter(
                property=property.property).aggregate(avg=Avg('rank'))
            viewed = MostViewed.objects.filter(property=property.property)
            if rank['avg'] is not None:
                rank = "{:.2f}".format(rank['avg'])
            else:
                rank = 0
            data = {
                'property': property.property,
                'rank': rank,
                'viewed': viewed[0].viewed,
            }
            context['properties'].append(data)
        return context


class createFeedbackView(CreateView):
    """
        Created feedback for a particular property.
    """
    model = FeedBackProperty
    form_class = FeedbackForm
    #template_name = 'feedback/create_feedback_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        property = Property.objects.get(
            slug=self.kwargs['slug'], property_status='published')
        data.property = property
        data.save()
        return redirect(reverse('realestateapp:detail_property', kwargs={'slug': data.property.slug}))


class createRankingView1(CreateView):
    """
        Give the ranck to a property.
    """
    model = RankingProperty
    form_class = RankingPropertyForm
    #template_name = 'ranking/create_ranking_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        property = RankingProperty.objects.filter(
            user=self.request.user, property__slug=self.kwargs['slug'], property__property_status='published')
        if not property:
            if data.rank > 5:
                return redirect('create_ranking_property', slug=self.kwargs['slug'])
            data.user = self.request.user
            property = Property.objects.get(
                slug=self.kwargs['slug'], property_status='published')
            data.property = property
            data.save()

        return redirect(reverse('realestateapp:detail_property', kwargs={'slug': self.kwargs['slug']}))


class createRankingView(CreateView):
    """
        Give the ranck to a property.
    """
    model = RankingProperty
    form_class = RankingPropertyForm
    template_name = 'ranking/create_ranking_property.html'

    def form_valid(self, form):
        data = form.save(commit=False)
        property = RankingProperty.objects.filter(
            user=self.request.user, property__slug=self.kwargs['slug'], property__property_status='published')
        if not property:
            if data.rank > 5:
                return redirect('create_ranking_property', slug=self.kwargs['slug'])
            data.user = self.request.user
            property = Property.objects.get(
                slug=self.kwargs['slug'], property_status='published')
            data.property = property
            data.save()

        return redirect(reverse('realestateapp:detail_property', kwargs={'slug': self.kwargs['slug']}))


class propertyNameSearchView(ListView):
    """
        Property wise search bar functionality.
    """
    template_name = 'property/search_with_property_name.html'
    model = Property

    def get_context_data(self, **kwargs):
        property = self.request.GET.get('property')
        context = super().get_context_data(**kwargs)
        context['propertiess'] = Property.objects.filter(
            property_name__icontains=property, property_status='published')
        context['properties'] = []
        for property in context['propertiess']:
            rank = RankingProperty.objects.filter(
                property=property).aggregate(avg=Avg('rank'))
            viewed = MostViewed.objects.filter(property=property)
            if rank['avg'] is not None:
                rank = "{:.2f}".format(rank['avg'])
            else:
                rank = 0
            data = {
                'property': property,
                'rank': rank,
                'viewed': viewed[0].viewed,
            }
            context['properties'].append(data)
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
        context['properties'] = Property.objects.filter(property_status='published').order_by(
            '-created_date')[:8]
        print(context['properties'])
        return context


class ListPropertyRankingWiseView(ListView):
    """
        Ranking wise hotels will be shown from this functions.
    """
    model = RankingProperty
    template_name = 'property/list_property_ranking_wise.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranking'] = RankingProperty.objects.filter(property__property_status='published').values(
            'property').annotate(avg=Avg('rank')).order_by('-avg')
        context['properties'] = []
        for item in context['ranking']:
            data = Property.objects.get(
                id=item['property'], property_status='published')
            context['properties'].append(data)
        return context


def createPropertyImages(request, slug):
    """
        This functionality for adding images of a particular property.
    """
    property = Property.objects.get(slug=slug)
    if request.method == "POST":
        images = ImagesProperty.objects.create(
            image=request.FILES['myFile'], property=property)
        images.save()
        return redirect(reverse('realestateapp:detail_property', kwargs={'slug': property.slug}))
    else:
        context = {}
        context['property'] = property
        return render(request, 'property/create_property_images.html', context)


class ListPropertyUserView(ListView):
    """
        List out the all properties.
    """
    template_name = 'property/list_property_user.html'
    model = Property
    #context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties'] = Property.objects.filter(
            author=self.request.user)
        context['propertiess'] = Property.objects.filter(
            author=self.request.user)
        context['properties'] = []
        for property in context['propertiess']:
            rank = RankingProperty.objects.filter(
                property=property).aggregate(avg=Avg('rank'))
            viewed = MostViewed.objects.filter(property=property)
            if rank['avg'] is not None:
                rank = "{:.2f}".format(rank['avg'])
            else:
                rank = 0
            data = {
                'property': property,
                'rank': rank,
                'viewed': viewed[0].viewed,
            }
            context['properties'].append(data)
        return context


class SearchCitylistProperty(ListView):
    """
        List out the all properties city wise.
    """
    template_name = 'property/city_list_property.html'
    model = Property
    context_object_name = 'properties'

    def get_queryset(self):
        city = self.kwargs['city']
        properties = Property.objects.filter(
            property_status='published', Address__city=city)
        return properties
