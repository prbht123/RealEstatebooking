from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Address, MostViewed, Property, Room, Address as Adrs, FeedBackProperty, RankingProperty
import json
# Create your tests here.


class TestViews(TestCase):
    def setUp(self):
        """
           This function will be execute firstly from another testing functions. 
        """
        self.client = Client()
        self.list_hotel_url = reverse('realestateapp:list_property')
        self.hotel_detail_url = reverse(
            'realestateapp:detail_property', args=['hotel1'])
        self.create_hotel_url = reverse('realestateapp:create_property')
        self.update_hotel_url = reverse(
            'realestateapp:Update_property', args=['hotel1'])
        self.delete_hotel_url = reverse(
            'realestateapp:delete_property', args=['hotel1'])
        self.list_mostviewed_hotel_url = reverse(
            'realestateapp:most_viewed_properties')
        self.create_feedback_url = reverse(
            'realestateapp:create_feedback_property', args=['hotel1'])
        self.user_1 = User.objects.create_user(
            'Chevy Chase',
            'chevy@chase.com',
            'chevyspassword'
        )
        self.roomtype = Room.objects.create(
            room_type_name="AC Room",
        )
        self.address = Adrs.objects.create(
            street="abc",
            city="kolkata",
            state="West bengal",
            country="India",
            zip_code="7653273",
        )
        self.hotel1 = Property.objects.create(
            property_name="hotel1",
            author=self.user_1,
            room_type=self.roomtype,
            bed_room=4,
            beds=4,
            bed_type="adult",
            guest=4,
            Address=self.address,
            cost=7562,
            property_status="draft",
            contact_number="623785287537",
            cancellation="free",
            Description="wgihiuehfiwquhfeiqu",
        )
        self.mostviewed = MostViewed.objects.create(
            property=self.hotel1,
            viewed=0,
        )

        self.feedback_hotel = FeedBackProperty.objects.create(
            property=self.hotel1,
            user=self.user_1,
            feedback="jgedkgweiuidwue",

        )
        self.rating_hotel = RankingProperty.objects.create(
            property=self.hotel1,
            user=self.user_1,
            rank=4,
        )

    def test_hotel_post(self):
        """
            This unit testing for creating new hotel.
        """
        response = self.client.post(self.create_hotel_url, {
            'property_name': "hotel2",
            'author': self.user_1,
            'room_type': self.roomtype,
            'bed_room': 4,
            'beds': 4,
            'bed_type': "adult",
            'guest': 4,
            'Address': self.address,
            'cost': 7562,
            'property_status': "draft",
            'contact_number': "623785287537",
            'cancellation': "free",
            'Description': "wgihiuehfiwquhfeiqu",
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'property/create_property.html')

    def test_hotels_list_get(self):
        """
            This unit testing for listing of Hotels.
        """
        response = self.client.get(self.list_hotel_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'property/list_property.html')

    def test_hotel_detail_get(self):
        """
            This unit testing for details of a hotel.
        """
        response = self.client.get(self.hotel_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'property/property_detail.html')

    def test_hotel_update(self):
        """
            This unit testing for updating of existing hotel.
        """
        response = self.client.put(self.update_hotel_url, {
            'property_name': "hotel2",
            'author': self.user_1,
            'room_type': self.roomtype,
            'bed_room': 5,
            'beds': 5,
            'bed_type': "adult",
            'guest': 5,
            'Address': self.address,
            'cost': 75872,
            'property_status': "draft",
            'contact_number': "623785287537",
            'cancellation': "free",
            'Description': "wgihiuiwugefiuwgeiuehfiwquhfeiqu",
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'property/property_update.html')

    def test_hotel_delete(self):
        """
            This unit testing for deleting of existing blog.
        """
        response = self.client.delete(self.delete_hotel_url)
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_mostviewed_hotels_list_get(self):
        """
            This unit testing for listing of Hotels which is most viewed.
        """
        response = self.client.get(self.list_mostviewed_hotel_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'property/most_viewed_all_properties.html')

    # def test_hotel_feedback_post(self):
    #     """
    #         This unit testing for giving feedback of a particular hotel.
    #     """
    #     response = self.client.post(self.create_feedback_url, {
    #         'property': self.hotel1,
    #         'user': self.user_1,
    #         'feedback': "jewfiugewiufgiweugfiugewi"

    #     })
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'feedback/create_feedback.html')

    # Model testing.......................

    def test_hotel_slug_module(self):
        """
            Testing for Property module.
        """
        self.assertEquals(self.hotel1.slug, 'hotel1')

    def test_hotel_address_slug_module(self):
        """
            Testing for Address module.
        """
        self.assertEquals(self.address.slug, 'abc')

    def test_hotel_roomtype_slug_module(self):
        """
            Testing for Hotel Room Type module.
        """
        self.assertEquals(self.roomtype.slug, 'ac-room')

    def test_hotel_mostviewed_module(self):
        """
            Testing for MostViewed Hotel module.
        """
        self.assertEquals(self.mostviewed.property, self.hotel1)

    def test_hotel_feedback_slug_module(self):
        """
            Testing for giving Feedback Hotel module.
        """
        self.assertEquals(self.feedback_hotel.property, self.hotel1)

    def test_hotel_ranking_slug_module(self):
        """
            Testing for Rating hotel module.
        """
        self.assertEquals(self.rating_hotel.property, self.hotel1)
