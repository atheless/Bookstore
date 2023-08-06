from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from projectdj.forms import MyUserCreationForm
from django.test import Client

from uprofile.forms import UserEditForm, SellerApplyForm


# Create your tests here.

class UserForm(TestCase):

    """
    Test user creation form.
    """
    def test_create_user_form(self):
        form_data = {'username': 'Test',
                     'first_name': 'Test',
                     'last_name': 'Test',
                     'email': 'ddsa@dasg.com',
                     'password1': 'tDwdWECWe2',
                     'password2': 'tDwdWECWe2',
                     }
        form = MyUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    """
    Test user edit form.
    """
    def test_user_edit_form(self):
        form_data = {
                     'first_name': 'Test',
                     'last_name': 'Test',
                     'email': 'ddsa@dasg.com',
                     }
        form = UserEditForm(data=form_data)
        self.assertTrue(form.is_valid())


class SellerForm(TestCase):

    """
    Test seller apply form.
    """
    def test_seller_apply_form_test1(self):
        form_data = {
            'seller_name': 'Test',
            'country': 'AZ',
            'legal_seller_address': 'asdsda',
            'contact_phone': '3213213',
            'seller_email': 'dawdsasd@gmai.com',
            'description': 'x'*100,
        }
        form = SellerApplyForm(data=form_data)
        self.assertTrue(form.is_valid())

    """
    Test seller name can not be empty.
    """
    def test_seller_apply_form_test2(self):
        form_data = {
            'seller_name': '',
            'country': 'Test',
            'legal_seller_address': 'ddsa@dasg**',
            'contact_phone': '3213213',
            'seller_email': 'dawd@gmai.com',
            'description': 'x'*100,
        }

        form = SellerApplyForm(data=form_data)
        self.assertFalse(form.is_valid())

    """
    Test seller legal address cannot contains special chars.
    """
    def test_legal_seller_address(self):
        form_data = {
            'seller_name': 'Test',
            'country': 'Test',
            'legal_seller_address': 'ddsa@dasg**',
            'contact_phone': '3213213',
            'seller_email': 'dawd@gmai.com',
            'description': 'x'*100,
        }

        form = SellerApplyForm(data=form_data)
        self.assertFalse(form.is_valid())

    """
    Test seller description  should contains at least 75 characters.
    """
    def test_seller_descrition(self):
        form_data = {
            'seller_name': 'Test',
            'country': 'Test',
            'legal_seller_address': 'ddsa@dasg**',
            'contact_phone': '3213213',
            'seller_email': 'dawd@gmai.com',
            'description': 'x',
        }

        form = SellerApplyForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestAccessCreationProduct(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='DpaDwdqwd!23', email='ates@tsr.com')
        self.client = Client()

    """
     Test access to the product creation page when user is not a seller.
    """

    def test_user_access(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('ushopping:create-product'), {'user_id': self.user.id})
        response2 = self.client.get(reverse('ushopping:create-product'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response2.status_code, 403)



class TestAccessManageApplications(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='DpaDwdqwd!23', email='ates@tsr.com')
        self.user.is_staff = 1
        self.client = Client()

    '''
    Test access to application management page when user is not staff.
    '''

    def test_user_access(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('uprofile:sellers-app-forms'), {'user_id': self.user.id})
        response2 = self.client.post(reverse('uprofile:sellers-app-forms'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response2.status_code, 403)

