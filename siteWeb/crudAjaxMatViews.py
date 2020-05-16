from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator


# Show Material
def indexView(request):
    """
    **Context**
    \nView all the materials and their information as a table.
    :param request: This request object contains information set by entities present before a view method.
    :return: Table with information of materials.
    """
    form = formMaterial()
    material = Material.objects.all()
    paginator = Paginator(material, per_page=6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'siteWeb/crudMaterial/ajaxCrudMat.html', {"form": form, "materials": page_obj.object_list, 'paginator': paginator, 'page_number': int(page_number)})