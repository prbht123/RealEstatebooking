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
        self.create_register_admin_user_url = reverse(
            'admin_user:admin_register_user')
        self.delete_adminuser_url = reverse(
            'admin_user:delete_users_by_admin', args=['1'])
        self.create_user_role_url = reverse(
            'admin_user:create_role', args=['1'])
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

    def test_rgister_admin_user_post(self):
        """
            This unit testing for registered new admin user by admin user.
        """
        response = self.client.post(self.create_register_admin_user_url, {
            'username': 'Chevy Chase heavy',
            'email': 'chevey@chase.com',
            'password': 'chevyspassword'
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/create_admin_register_user.html')

    def test_admin_delete_normaluser_delete(self):
        """
                This unit testing for deleting normal user by admin user.
        """
        response = self.client.delete(self.delete_adminuser_url)
        self.assertRedirects(response, '/adminuser/normalusers/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_create_user_role_post(self):
        """
            This unit testing for created role to admin user by admin user.
        """
        response = self.client.post(self.create_user_role_url, {
            'roles': 'Chevy Chase heavy',
            'user': self.user_1
        })
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'admin/roles/create_role_admin_user.html')
