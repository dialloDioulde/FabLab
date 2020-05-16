from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Loaner
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan


# Show Type
def TypeView(request):
    """
    **Context**
    \nShow table of all Types created and their description.

    :param request: This request object contains information set by entities present before a view method.
    :return: Table with specific information for each type saved.
    """
    form = formType()
    type = Type.objects.all()
    paginator = Paginator(type, per_page=6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'siteWeb/type/ajaxCrudType.html', {"form": form, "types": page_obj.object_list, 'paginator': paginator, 'page_number': int(page_number)})


# Create Type
class CreateCrudType(View):
    """
    **Context**
    \nCreate a new Type. Specify the information needed to create a new type, such as: name, description and if the type
    id UNIQUE or GENERIC.
    \nUnique: Only ONE material can be generated by this type, which means a type specified as Unique
    is used only once.
    \nGeneric: Multiple materials can be generated from this Type. There are multiple materials in the Inventory of FabLab
    of the same type.
    """
    def get(self, request):
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
    """
    **Context**
    \n Update of the specific Type.
    """
    def get(self, request):
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
    """
    **Context**
    \nDelete a Type object from the inventory.
    """
    def  get(self, request):
        id_type = request.GET.get('id', None)
        Type.objects.get(id = id_type).delete()
        data = {'deleted': True}
        return JsonResponse(data)