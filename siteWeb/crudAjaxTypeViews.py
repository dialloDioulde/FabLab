from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Loaner
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan



# Show Type
class TypeView(TemplateView):
    template_name = 'siteWeb/type/ajaxCrudType.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context


# Create Type
class CreateCrudType(View):
    def  get(self, request):
        material_type = request.GET.get('material_type', None)
        name_type = request.GET.get('name_type', None)
        description = request.GET.get('description', None)

        obj = Type.objects.create(material_type = material_type, name_type = name_type, description = description)

        type = {'id':obj.id,'material_type':obj.material_type,'name_type':obj.name_type,'description':obj.description}

        data = {
            'type': type
        }
        return JsonResponse(data)


# Update Type
class UpdateCrudType(View):
    def  get(self, request):
        id = request.GET.get('id_type', None)
        material_type_e = request.GET.get('material_type', None)
        name_type_e = request.GET.get('name_type', None)
        description_e = request.GET.get('description', None)

        obj = Type.objects.get(id = id)
        obj.material_type = material_type_e
        obj.name_type = name_type_e
        obj.description = description_e

        obj.save()

        type = {'id':obj.id,'material_type':obj.material_type,'name_type':obj.name_type,'description':obj.description}


        data = {
            'type': type
        }
        return JsonResponse(data)



# Delete Type
class DeleteCrudType(View):
    def  get(self, request):
        id_type = request.GET.get('id', None)
        Type.objects.get(id = id_type).delete()
        data = {'deleted': True}
        return JsonResponse(data)