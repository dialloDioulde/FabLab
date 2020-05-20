from itertools import chain

from django.db.models import QuerySet
from django.test import TestCase, Client
from django.contrib.auth.models import User
from siteWeb.views import *
from django.urls import reverse, resolve
from siteWeb.forms import *
from siteWeb import views, crudAjaxLoanerViews, crudAjaxMatViews, crudAjaxTypeViews
from siteWeb.models import Loaner, Type, Material, LoanMaterial, Loan, UserProfile
import json


class TestsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_homepage = reverse('homepage')
        self.url_register = reverse('register')
        self.url_login = reverse('login')

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        Loaner.objects.create(last_name='Franck', first_name='badoz', email='franck@badoz.fr', establishment='WIC')

        Type.objects.create(material_type='generic', name_type='Impri1', description='Fragile')
        self.type_data = Type.objects.get(id=1)

        Material.objects.create(name='Tablette', barcode="AA876BG", type=Type.objects.get(id=1))
        self.material_data = Material.objects.get(id=1)

        LoanMaterial.objects.create(user=test_user1, material=Material.objects.get(id=1), quantity=5)
        self.loan_material_data = LoanMaterial.objects.get(id=1)



    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)


    def test_views_get_home_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        response = self.client.get(self.url_homepage)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('materials' in response.context)
        self.assertTrue('search_term' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/home.html')


    def test_views_get_register_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK') # Login user
        response = self.client.get(self.url_register)
        self.assertEqual(response.status_code, 302)
        #self.assertTemplateUsed(response, 'siteWeb/accounts/register.html')


    def test_views_get_showProfile_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('showProfile'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.context)
        self.assertFalse('form' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/accounts/showProfile.html')


    def test_views_get_editProfile_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('editProfile'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/accounts/editProfile.html')


    def test_views_get_change_password_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('change-password'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/accounts/changePassword.html')



    def test_views_get_add_material_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('addMaterial'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/addMaterial.html')


    def test_views_get_update_material_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('updateMaterial', args=[1]))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed(response, 'siteWeb/addMaterial.html')


    def test_views_get_all_loan_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('allLoan'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('loan_all' in response.context)
        self.assertTrue('page_number' in response.context)
        self.failUnless(isinstance(response.context['loan_all'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/all_Loan.html')


    def test_views_get_loan_not_returned_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('notReturnedLoan'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginator_2' in response.context)
        self.assertTrue('loan_not_ret' in response.context)
        self.assertTrue('page_number_2' in response.context)
        self.failUnless(isinstance(response.context['loan_not_ret'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/loan_not_returned.html')


    def test_views_get_loan_surpassed_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('LoanSurpassed'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginator_3' in response.context)
        self.assertTrue('loan_surpassed' in response.context)
        self.assertTrue('page_number_3' in response.context)
        self.failUnless(isinstance(response.context['loan_surpassed'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/loan_surpassed.html')


    def test_views_get_loaner_views_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('LoanerView'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('loaners' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('page_number' in response.context)
        self.failUnless(isinstance(response.context['loaners'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/loaner/ajaxCrudLoaner.html')


    def test_views_get_type_views_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('TypeView'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('types' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('page_number' in response.context)
        self.failUnless(isinstance(response.context['types'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/type/ajaxCrudType.html')


    def test_views_get_material_views_page(self):
        """
            Here we check that the viwes returns the specified good behavior,
            ie the templates, the data sent in the context or args.
        """
        # Login user
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('MaterialView'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        print(response.context['paginator'])
        self.assertTrue('paginator' in response.context)
        self.assertTrue('materials' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('page_number' in response.context)
        self.failUnless(isinstance(response.context['materials'], QuerySet))
        self.assertTemplateUsed(response, 'siteWeb/crudMaterial/ajaxCrudMat.html')

