from django.test import TestCase, Client
from django.contrib.auth.models import User
from siteWeb.views import *
from siteWeb.models import *
from django.urls import reverse, resolve

from siteWeb.models import Loaner, Type, Material, LoanMaterial, Loan, UserProfile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {'username': 'username', 'email_adress': 'user@test.fr', 'password': 'password',
                     'password_confirmation': 'password'}

        return super().setUp()


class UserTest(BaseTest):

    # User Register test
    def test_user_register(self):
        response = self.client.post(self.register_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)


    # User Login test
    def test_user_login(self):
        c = Client()
        c.login(username='username', password='password')
        response = c.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)



class TestsModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(username='user1', password='7567fdh67TDF')
        test_user1.save()
        Loaner.objects.create(last_name = 'Franck', first_name = 'badoz', email = 'franck@badoz.fr', establishment = 'WIC')
        Type.objects.create(material_type = 'generic', name_type = 'Impri1', description = 'Fragile')
        Material.objects.create(name = 'Tablette', barcode = "AA876BG", type = Type.objects.get(id=1))
        LoanMaterial.objects.create(user = test_user1, material = Material.objects.get(id=1), quantity = 5)

        #Loan.objects.create(user = test_user1, loaner = Loaner.objects.get(id=1)), Material.set(LoanMaterial.objects.get(id=1), expected_return_date= '12/06/2020')
        #print(Loan)


    # Start of the Loaner Models Label Fields test
    def test_last_name_label(self):
        loaner = Loaner.objects.get(id=1)
        field_label = loaner._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')


    def test_first_name_label(self):
        loaner = Loaner.objects.get(id=1)
        field_label = loaner._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')


    def test_email_label(self):
        loaner = Loaner.objects.get(id=1)
        field_label = loaner._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email')


    def test_establishment_label(self):
        loaner = Loaner.objects.get(id=1)
        field_label = loaner._meta.get_field('establishment').verbose_name
        self.assertEquals(field_label, 'establishment')

    def test_creation_date_max_length(self):
        loaner = Loaner.objects.get(id=1)
        field_label = loaner._meta.get_field('creation_date').verbose_name
        self.assertEquals(field_label, 'creation date')

    # End of the Loaner Models Label Fields test


    # Start of the  Loaner Models Field Length test
    def test_last_name_max_length(self):
        loaner = Loaner.objects.get(id=1)
        max_length = loaner._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 255)

    def test_first_name_max_length(self):
        loaner = Loaner.objects.get(id=1)
        max_length = loaner._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 255)

    def test_email_max_length(self):
        loaner = Loaner.objects.get(id=1)
        max_length = loaner._meta.get_field('email').max_length
        self.assertEquals(max_length, 255)


    def test_establishment_max_length(self):
        loaner = Loaner.objects.get(id=1)
        max_length = loaner._meta.get_field('establishment').max_length
        self.assertEquals(max_length, 250)

    # End of the  Loaner Models Field Length test

    # Start Test of the str() function of the Loaner Models
    def test_get_last_name_first_name(self):
        loaner = Loaner.objects.get(id=1)
        expected_object_loaner = f'{loaner.last_name} {loaner.first_name}'
        self.assertEquals(expected_object_loaner, str(loaner))

    # End of the Test of the str() function of the Loaner Models

    # Start of the Type Models Label Fields test
    def test_material_type_label(self):
        type_material = Type.objects.get(id=1)
        field_label = type_material._meta.get_field('material_type').verbose_name
        self.assertEquals(field_label, 'material type')


    def test_name_type_label(self):
        type_material = Type.objects.get(id=1)
        field_label = type_material._meta.get_field('name_type').verbose_name
        self.assertEquals(field_label, 'name type')


    def test_description_type_label(self):
        type_material = Type.objects.get(id=1)
        field_label = type_material._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')


    def test_creation_date_type_label(self):
        type_material = Type.objects.get(id=1)
        field_label = type_material._meta.get_field('creation_date_type').verbose_name
        self.assertEquals(field_label, 'creation date type')


    def test_unavailable_type_label(self):
        type_material = Type.objects.get(id=1)
        field_label = type_material._meta.get_field('unavailable').verbose_name
        self.assertEquals(field_label, 'unavailable')

    # End of the Type Models Label Fields test

    # Start of the  Type Models Field Length test
    def test_material_type_max_length(self):
        type_material = Type.objects.get(id=1)
        max_length = type_material._meta.get_field('material_type').max_length
        self.assertEquals(max_length, 250)

    def test_name_type_max_length(self):
        type_material = Type.objects.get(id=1)
        max_length = type_material._meta.get_field('name_type').max_length
        self.assertEquals(max_length, 250)

    def test_description_max_length(self):
        type_material = Type.objects.get(id=1)
        max_length = type_material._meta.get_field('description').max_length
        self.assertEquals(max_length, None)

    # End of the  Type Models Field Length test

    # Start Test of the str() function of the Type Models
    def test_get_name_type_material_type(self):
        type_material = Type.objects.get(id=1)
        expected_object_type = f'{type_material.name_type} - {type_material.material_type}'
        self.assertEquals(expected_object_type, str(type_material))

    # End of the Test of the str() function of the Type Models

    # Start of the Material Models Label Fields test
    def test_name_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_barcode_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('barcode').verbose_name
        self.assertEquals(field_label, 'barcode')

    def test_creation_date_mat_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('creation_date_mat').verbose_name
        self.assertEquals(field_label, 'creation date mat')

    def test_slug_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_material_picture_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('material_picture').verbose_name
        self.assertEquals(field_label, 'material picture')

    def test_type_label(self):
        material = Material.objects.get(id=1)
        field_label = material._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    # End of the Material Models Label Fields tes

    # Start of the  Material Models Field Length test
    def test_name_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)

    def test_barcode_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('barcode').max_length
        self.assertEquals(max_length, 50)

    def test_creation_date_mat_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('creation_date_mat').max_length
        self.assertEquals(max_length, None)

    def test_slug_mat_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('slug').max_length
        self.assertEquals(max_length, 250)

    def test_material_picture_mat_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('material_picture').max_length
        self.assertEquals(max_length, 100)

    def test_type_mat_max_length(self):
        material = Material.objects.get(id=1)
        max_length = material._meta.get_field('type').max_length
        self.assertEquals(max_length, None)

    # End of the  Material Models Field Length test

    # Start Test of the str() function of the Material Models
    def test_get_name_id(self):
        material = Material.objects.get(id=1)
        expected_object_material = f'{material.name} (id:  {material.id})'
        self.assertEquals(expected_object_material, str(material))

    # End of the Test of the str() function of the Material Models

    # Start Test of the get_absolute_url() function of the Material Models
    #def test_get_absolute_url(self):
        #material = Material.objects.get(id=1)
        #expected_object_material = f'{material.name} (id:  {material.id})'
        #self.assertEquals(str(material.get_absolute_url), "Material: " + expected_object_material)

    # End of the Test of the get_absolute_url() function of the Material Models


    # Start of the Loan Material Models Label Fields test
    def test_user_label(self):
        loan_material = LoanMaterial.objects.get(id=1)
        field_label = loan_material._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_ordered_label(self):
        loan_material = LoanMaterial.objects.get(id=1)
        field_label = loan_material._meta.get_field('ordered').verbose_name
        self.assertEquals(field_label, 'ordered')

    def test_material_label(self):
        loan_material = LoanMaterial.objects.get(id=1)
        field_label = loan_material._meta.get_field('material').verbose_name
        self.assertEquals(field_label, 'material')

    def test_quantity_label(self):
        loan_material = LoanMaterial.objects.get(id=1)
        field_label = loan_material._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')

    def test_creation_date_loan_mat_label(self):
        loan_material = LoanMaterial.objects.get(id=1)
        field_label = loan_material._meta.get_field('creation_date_loan_mat').verbose_name
        self.assertEquals(field_label, 'creation date loan mat')

    # End of the Loan Material Models Label Fields test


    # Start of the  Loan Material Models Field Length test
    def test_user_max_length(self):
        loan_material = LoanMaterial.objects.get(id=1)
        max_length = loan_material._meta.get_field('user').max_length
        self.assertEquals(max_length, None)

    def test_ordered_max_length(self):
        loan_material = LoanMaterial.objects.get(id=1)
        max_length = loan_material._meta.get_field('ordered').max_length
        self.assertEquals(max_length, None)

    def test_material_max_length(self):
        loan_material = LoanMaterial.objects.get(id=1)
        max_length = loan_material._meta.get_field('material').max_length
        self.assertEquals(max_length, None)

    def test_quantity_max_length(self):
        loan_material = LoanMaterial.objects.get(id=1)
        max_length = loan_material._meta.get_field('quantity').max_length
        self.assertEquals(max_length, None)

    def test_creation_date_loan_mat_max_length(self):
        loan_material = LoanMaterial.objects.get(id=1)
        max_length = loan_material._meta.get_field('creation_date_loan_mat').max_length
        self.assertEquals(max_length, None)

    # End of the  Loan Material Models Field Length test

    # Start Test of the str() function of the Loan Material Models
    def test_get_quantity_material_name(self):
        loan_material = LoanMaterial.objects.get(id=1)
        expected_object_material = f'{loan_material.quantity} {loan_material.material.name}'
        self.assertEquals(expected_object_material, str(loan_material))

    # End of the Test of the str() function of the Loan Material Models


