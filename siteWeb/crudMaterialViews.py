from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Loaner
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan
from django.template.loader import render_to_string
from django.http import JsonResponse

# Show Material
def crudShowMaterial(request):
    material = Material.objects.all()
    context = {'materials': material}
    return render(request, 'siteWeb/material/ajaxCrudMaterial.html', context)


def crudCreateMaterial(request):
    form = formMaterial()
    context = {'form': form}
    create_material = render_to_string('siteWeb/material/ajaxCreateMaterial.html', context, request=request)
    return JsonResponse({'create_material': create_material})

