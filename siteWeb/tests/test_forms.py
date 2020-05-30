from django.test import SimpleTestCase, TestCase, Client
from siteWeb.forms import *
from django.conf import settings



class TestsForms(TestCase):

    # Creations Data
    @classmethod
    def setUp(self):
        test_user1 = User.objects.create_user(username='user1', password='7567fdh67TDF')
        self.user = User.objects.get(id=1)

        Loaner.objects.create(last_name='Franck', first_name='badoz', email='franck@badoz.fr', establishment='WIC')
        self.loaner = Loaner.objects.get(id=1)

        Type.objects.create(material_type='generic', name_type='Impri1', description='Fragile')
        self.type_data = Type.objects.get(id=1)

        Material.objects.create(name='Tablette', barcode="AA876BG", type=Type.objects.get(id=1))
        self.material_data = Material.objects.get(id=1)

        LoanMaterial.objects.create(user=test_user1, material=Material.objects.get(id=1), quantity=5)
        self.loan_material_data = LoanMaterial.objects.get(id=1)


    # Start of the test for the Loaner form
    def test_loaner_form_valid_data(self):
        form = formLoaner(data = {'last_name': 'Junior', 'first_name': 'DIALLO', 'email': 'junior@diallo.fr', 'establishment': 'WIC UGA'})
        self.assertTrue(form.is_valid())

    def test_loaner_form_no_data(self):
        form = formLoaner(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # End of the test for the Loaner form


    # Start of the test for the Type form
    def test_type_form_valid_data(self):
        form = formType(data = {'material_type': 'generic', 'name_type': 'Impri3', 'description': 'Fragile'})
        self.assertTrue(form.is_valid())

    def test_type_form_no_data(self):
        form = formType(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    # End of the test for the Type form


    # Start of the test for the Material form
    def test_material_form_valid_data(self):
        form = formMaterial(data = {'name': 'Imprimente 3D', 'barcode': 'BD7456TF', 'type': self.type_data.pk})
        self.assertTrue(form.is_valid())
        form.save()

    def test_material_form_no_data(self):
        form = formMaterial(data = {})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    # End of the test for the Material form


    # Start of the test for the Loan Material form
    def test_loan_material_form_valid_data(self):
        form = formLoanMaterial(data={'user': self.user.pk, 'material': self.material_data.pk , 'quantity': '10'})
        self.assertTrue(form.is_valid())
        #form.save()

    def test_loan__material_form_no_data(self):
        form = formLoanMaterial(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    # End of the test for the Loan Material form


    # Start of the test for the Loan form
    def test_loan_form_valid_data(self):
        form = formLoan(data={'user': self.user.pk, 'loaner': self.loaner.pk, 'materials': self.material_data.pk , 'expected_return_date': '12/06/2020'})
        self.assertTrue(form.is_valid())

    def test_loan_form_no_data(self):
        form = formLoan(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    # End of the test for the Loan form
