from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PopularLocations, AdminUserRoles
# Create your tests here.


class TestViews(TestCase):
    def setUp(self):
        """
           This function will be execute firstly from another testing functions. 
        """
        self.client = Client()
        self.admin_user_list_url = reverse('admin_user:admin_manage_users')
        self.normal_user_list_url = reverse('admin_user:normal_users')
        self.aaproving_hotels_list_url = reverse(
            'admin_user:approving_property_list')
        self.user_1 = User.objects.create_user(
            'Chevy Chase heavy',
            'chevey@chase.com',
            'chevyspassword'
        )
        self.user_1.is_staff = True

    def test_adminuser_list_get(self):
        """
            This unit testing for listing of Admin Users.
        """
        response = self.client.get(self.admin_user_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/adminManageUser.html')

    def test_normaluser_list_get(self):
        """
            This unit testing for listing of normal Users.
        """
        response = self.client.get(self.normal_user_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/users/list_users.html')

    def test_approving_hotel_list_get(self):
        """
            This unit testing for listing of normal Users.
        """
        response = self.client.get(self.aaproving_hotels_list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'admin/approving_property/list_draft_property.html')
