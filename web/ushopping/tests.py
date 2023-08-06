
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test import Client

from django.urls import reverse

from ushopping.models import Product, Category, Cart


class ModelProductTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

        self.C = Category.objects.create(name='TestCategory')
        Product.objects.create(user=self.user, category=self.C, name='T', year=123, price=23)

    """
    Number of products created should be equal to 1
    """
    def test_number_products_created(self):
        self.assertEqual(Product.objects.all().count(), 1)

    """
    New product must be part of a category.
    """

    def test_new_product_must_have_category(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(user=self.user)



class ModelCategoryTests(TestCase):

    """
    Category name can not be empty.
    """
    def test_name_not_null(self):
        self.assertTrue(Category.objects.create(name='Test'))
        

class TestDeleteOtherCartProducts(TestCase):
    """
    Init: Create User1 and User2. Create a new Category 'Horror' and Product with a name 'Green'.
    User1 will add a product with a name 'Green' to his cart.
    """
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='DpaDwdqwd!23', email='ates@tsr.com')
        self.user2 = User.objects.create(username='user2', password='DpaDwdqwd!23', email='atddaes@tsr.com')
        self.category = Category.objects.create(name='Horror')
        self.product = Product.objects.create(user=self.user1, category=self.category, name='Green', year='1992',
                                              publisher='dqw', condition='0', short_description='w', description='2', price='22')
        self.user1cart = Cart.objects.create(user=self.user1, amount=1, item=self.product)
        self.client = Client()

    """
    Test: User2 will try to delete cart item of User1. System should reject any actions from User1.
    """
    def test_user2_deletes_cartItem_of_user_1(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('ushopping:cart-delete-view', kwargs={'pk': 1}), {'user_id': self.user2.id})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    """
    Test: User1 will try to delete item from his cart. System should allow this type of action. 
    """
    def test_user1_access_to_his_delete_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('ushopping:cart-delete-view', kwargs={'pk': 1}), {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        

