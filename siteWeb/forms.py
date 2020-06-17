from django import forms
from siteWeb.models import Loan,Loaner,Material,LoanMaterial,Type
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


# Formualire d'Insciption d'Utilisateur
class formLoaner(forms.ModelForm):
    class Meta:
        # model generated based on table Loaner
        model = Loaner
        # show specific fields on the automatically generated form (based on model)
        fields = ['last_name', 'first_name', 'email','establishment']


# Formulaire d'Ajout Des Type De Materiels
class formType(forms.ModelForm):
    class Meta:
        # model generated based on table Type
        model = Type
        # exculde field form showing on the automatically generated form (based on model)
        exclude = ['creation_date_type', 'unavailable']


# Formulaire d'Ajout De Materiels
class formMaterial(forms.ModelForm):
    # on the type field of the model Material, the field (drowdown) type is going to have filters applied to them
    type = forms.ModelChoiceField(queryset=Type.objects.filter(unavailable=False).order_by('material_type'))

    class Meta:
        # model generated based on table Material
        model = Material
        # show specific fields on the automatically generated form (based on model)
        fields = ['name','barcode','type', 'material_picture']


class formLoanMaterial(forms.ModelForm):
    class Meta:
        # model generated based on table LoanMaterial
        model = LoanMaterial
        # show specific fields on the automatically generated form (based on model)
        fields = ['material','quantity']


class NewUserForm(UserCreationForm):
    # automatically generated Creation Form
    # create a New User. Form to add a new Staff Member
    email = forms.EmailField(required=True)
    establishment = forms.CharField(required=True)

    class Meta:
        # model generated based on table User
        model = User
        # show specific fields on the automatically generated form (based on model)
        fields = ("username", "email", "establishment", "password1", "password2")

    def save(self, commit=True):
        # save user
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.establishment = self.cleaned_data['establishment']
        if commit:
            user.save()
        return user


# Edit Profile
class EditProfileForm(UserChangeForm):
    # automatically generated Change Form
    class Meta:
        # model generated based on table User
        model = User
        # show specific fields on the automatically generated form (based on model)
        fields = ("username", "first_name", "last_name", "email")


class DateInput(forms.DateInput):
    input_type = 'date'


# Ajouter loaner to Loan
class formLoan(forms.ModelForm):
    expected_return_date = forms.DateField(widget=DateInput)

    class Meta:
        # model generated based on table Loan
        model = Loan
        labels = {
            'loaner': 'Borrower',
        }
        # show specific fields on the automatically generated form (based on model)
        fields = ('loaner', 'expected_return_date')

