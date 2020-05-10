from django import forms
from siteWeb.models import Loan,Loaner,Material,LoanMaterial,Type
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


# Formualire d'Insciption d'Utilisateur
class formLoaner(forms.ModelForm):
    class Meta:
        model = Loaner
        fields = ['last_name', 'first_name', 'email','establishment']


# Formulaire d'Ajout Des Type De Materiels
class formType(forms.ModelForm):
    class Meta:
        model = Type
        exclude = ['creation_date_type']


# Formulaire d'Ajout De Materiels Uniques
class formUnique(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name','barcode', 'material_picture']


# Formulaire d'Ajout De Materiels
class formMaterial(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Type.objects.filter(unavailable=False).order_by('material_type'))

    class Meta:
        model = Material
        fields = ['name','barcode','type', 'material_picture']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['type'].queryset = Type.objects.filter(material_type='generic')


class formLoanMaterial(forms.ModelForm):
    class Meta:
        model = LoanMaterial
        fields = ['material','quantity']


# Formulaire d'Ajout d'un Emprunt
class formLoan(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loaner','materials','expected_return_date', 'return_date']


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    establishment = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "establishment", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.establishment = self.cleaned_data['establishment']
        if commit:
            user.save()
        return user


class DateInput(forms.DateInput):
    input_type =  'date'


#Ajouter loaner to Loan
class formLoan(forms.ModelForm):
    expected_return_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Loan
        fields = ('loaner', 'expected_return_date')

