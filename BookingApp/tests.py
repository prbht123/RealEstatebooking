from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from RealEstateApp.models import Address, MostViewed, Property, Room, Address as Adrs
from .models import Booking
import json
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core import mail
# Create your tests here.


class TestViews(TestCase):
    def setUp(self):
        """
           This function will be execute firstly from another testing functions. 
        """
        self.client = Client()
        self.book_hotel_url = reverse(
            'booking:create_booking', args=['hotel1'])
        self.contact_url = reverse('booking:contact')
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
        self.timein = timezone.now()
        self.timeout = timezone.now()
        self.book1 = Booking.objects.create(
            gender="male",
            firstname="mohan",
            lastname="kumar",
            nationality="Indian",
            date_until=self.timeout,
            email="pp@gmail.com",
            address=self.address,
            cost=7562,
            mobile_Number="623785287537",
            date_from=self.timeout,
            notes="wgihiuehfiwquhfeiqu",
            booking_status="initiated",
            property=self.hotel1,
            paid=False,
        )

        self.update_book_hotel_url = reverse(
            'booking:Update_booking', kwargs={'slug': self.book1.slug})
        self.delete_booked_hotel_url = reverse(
            'booking:delete_booking', kwargs={'slug': self.book1.slug})

        self.mailsend = send_mail(
            "subject", "msg", settings.EMAIL_HOST_USER, ['prabhat.webkrone@gmail.com'])

    def test_hotel_book_post(self):
        """
            This unit testing for booking new hotel.
        """
        response = self.client.post(self.book_hotel_url, {
            'gender': "male",
            'firstname': "mohan",
            'lastname': "kumar",
            'nationality': "Indian",
            'date_until': "",
            'email': "pp@gmail.com",
            'address': self.address,
            'cost': 7562,
            'mobile_Number': "623785287537",
            'date_from': "",
            'notes': "wgihiuehfiwquhfeiqu",
            'booking_status': "initiated",
            'property': self.hotel1,

        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/create_booking.html')

    def test_booked_hotel_update(self):
        """
            This unit testing for updating of bookied hotel.
        """
        response = self.client.put(self.update_book_hotel_url, {
            'gender': "female",
            'firstname': "mohini",
            'lastname': "kumari",
            'nationality': "Indian",
            'date_until': self.timein,
            'email': "pp@gmail.com",
            'cost': 752,
            'mobile_Number': "6285287537",
            'date_from': self.timein,
            'notes': "wgihiiuedkjwhakhfkwuehfiwquhfeiqu",
            'booking_status': "initiated",
            'property': self.hotel1,
            'city': "yuwu",
            'street': "igiefwke",
            'state': "dfgweiue",
            'country': "India",
            'zip_code': "36258732",

        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/update_booking.html')

    def test_hotel_booked_delete(self):
        """
            This unit testing for deleting of booked hotel.
        """
        response = self.client.delete(self.delete_booked_hotel_url)
        self.assertRedirects(response, '/home/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    # def test_contact_post(self):
    #     """
    #         This unit testing for sending mail from contact page.
    #     """
    #     response = self.client.post(self.contact_url, {
    #         'name': "mohan",
    #         'email': "prabhat.webcrone@gmail.com",
    #         'mobile_Number': "623785287537",
    #         'messages': "egwfkgweiufhiwuhfiuhwifhw"

    #     })
    #     print(response)
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'homepage/contact.html')

    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.', 'prabhat.webcrone@gmail.com',
                       ['prabhat.webkrone@gmail.com'])
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'subject')

    # Model testing.......................

    def test_booking_slug_module(self):
        """
            Testing for Booking module.
        """
        self.assertEquals(self.book1.slug, self.book1.slug)
