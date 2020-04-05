from django import forms
from siteWeb.models import Loan,Loaner,Material,LoanMaterial,Type,UserProfile


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


# Formulaire d'Ajout De Materiels
class formMaterial(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name','barcode','slug','material_picture','type']



class formLoanMaterial(forms.ModelForm):
    class Meta:
        model = LoanMaterial
        fields = ['material','quantity']

# Formulaire d'Ajout d'un Emprunt
class formLoan(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loaner','materials','expected_return_date', 'return_date']
