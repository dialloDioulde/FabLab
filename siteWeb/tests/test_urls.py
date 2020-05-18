from django.test import TestCase
from django.urls import reverse, resolve
from siteWeb.views import *
from siteWeb.crudAjaxTypeViews import *
from siteWeb.crudAjaxMatViews import *
from siteWeb.crudAjaxLoanerViews import *


class TestUrls(TestCase):

    # Home Page
    def test_homepage_url(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    # Register url test
    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)
        print(resolve(url))

    # Login url test
    def test_login_url(self):
        url = reverse('login')
        #self.assertEquals(resolve(url).func, login_request)

    # Logout url test
    def test_logout_url(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_request)

    # Show User Profil url test
    def test_showProfile_url(self):
        url = reverse('showProfile')
        self.assertEquals(resolve(url).func, showProfile)

    # Edit User Profil url test
    def test_editProfile_url(self):
        url = reverse('editProfile')
        self.assertEquals(resolve(url).func, editProfile)

    # User Change Password
    def test_change_password_url(self):
        url = reverse('change-password')
        self.assertEquals(resolve(url).func, change_password)

    # Add Material url test
    def test_addMaterial_url(self):
        url = reverse('addMaterial')
        self.assertEquals(resolve(url).func, addMaterial)

    # Edit Material url test
    def test_updateMaterial_url(self):
        url = reverse('updateMaterial', args=[1])
        self.assertEquals(resolve(url).func, updateMaterial)
        print(url)

    # Delete Material url test
    def test_deleteMaterial_url(self):
        url = reverse('DeleteCrudMaterial')
        self.assertEquals(resolve(url).func.view_class, DeleteCrudMaterial)

    # Show All Loan url test
    def test_allLoan_url(self):
        url = reverse('allLoan')
        self.assertEquals(resolve(url).func, allLoan)

    # Not Returned Loan url test
    def test_notReturned_Loan_url(self):
        url = reverse('notReturnedLoan')
        self.assertEquals(resolve(url).func, notReturnedLoan)

    # Loan Surpassed Loan url test
    def test_loan_surpassed_url(self):
        url = reverse('LoanSurpassed')
        self.assertEquals(resolve(url).func, LoanSurpassed)

    # Loan url test
    def test_loan_id_url(self):
        url = reverse('loan_id', args=[1])
        self.assertEquals(resolve(url).func, loan)

    # Update Loan url test
    def test_update_loan_url(self):
        url = reverse('updateLoan', args=[1])
        self.assertEquals(resolve(url).func, updateLoan)

    # Delete Loan url test
    def test_delete_loan_url(self):
        url = reverse('DeleteCrudLoan')
        self.assertEquals(resolve(url).func.view_class, DeleteCrudLoan)

    # Show Loaner url test
    def test_show_Loaner_url(self):
        url = reverse('LoanerView')
        self.assertEquals(resolve(url).func, LoanerView)

    # Create Loaner url test
    def test_create_loaner_url(self):
        url = reverse('CreateCrudLoaner')
        self.assertEquals(resolve(url).func.view_class, CreateCrudLoaner)

    # Edit Loaner url test
    def test_update_loaner_url(self):
        url = reverse('UpdateCrudLoaner')
        self.assertEquals(resolve(url).func.view_class, UpdateCrudLoaner)


    # Delete Loaner url test
    def test_delete_loaner_url(self):
        url = reverse('DeleteCrudLoaner')
        self.assertEquals(resolve(url).func.view_class, DeleteCrudLoaner)


    # Show Type url test
    def test_show_type_url(self):
        url = reverse('TypeView')
        self.assertEquals(resolve(url).func, TypeView)

    # Create Type url test
    def test_create_type_url(self):
        url = reverse('CreateCrudType')
        self.assertEquals(resolve(url).func.view_class, CreateCrudType)

    # Edit Type url test
    def test_update_type_url(self):
        url = reverse('UpdateCrudType')
        self.assertEquals(resolve(url).func.view_class, UpdateCrudType)


    # Delete Type url test
    def test_delete_type_url(self):
        url = reverse('DeleteCrudType')
        self.assertEquals(resolve(url).func.view_class, DeleteCrudType)


    # Show Material url test
    def test_show_material_url(self):
        url = reverse('MaterialView')
        self.assertEquals(resolve(url).func, indexView)

    # Material Detail url test
    def test_material_detail_url(self):
        url = reverse('material', args=[1])
        self.assertEquals(resolve(url).func.view_class, MaterialDetailView)


    # Add To Loan url test
    def test_add_to_loan_url(self):
        url = reverse('add-to-loan', args=[1])
        self.assertEquals(resolve(url).func, add_to_loan)


    # Remove From To Loan url test
    def test_remove_from_to_loan_url(self):
        url = reverse('remove-from-loan', args=[1])
        self.assertEquals(resolve(url).func, remove_from_loan)


    # Add One Material
    def test_add_one_material_url(self):
        url = reverse('add-one-material', args=[1])
        self.assertEquals(resolve(url).func, add_one_material)


     # Loans url test
    def test_loans_url(self):
        url = reverse('loan')
        self.assertEquals(resolve(url).func.view_class, loan_form)


    # Remove Material From Loan url test
    def test_remove_material_from_loan_url(self):
        url = reverse('remove-material-from-loan', args=[1])
        self.assertEquals(resolve(url).func, remove_single_item_from_loan)


    # Loan Summary url test
    def test_loan_summary_url(self):
        url = reverse('loan-summary')
        self.assertEquals(resolve(url).func.view_class, LoanSummaryView)


    # Edit Loan Summary url test
    def test_edit_loan_summary_url(self):
        url = reverse('edit-loan-summary', args=[1])
        self.assertEquals(resolve(url).func.view_class, EditLoanSummaryView)
