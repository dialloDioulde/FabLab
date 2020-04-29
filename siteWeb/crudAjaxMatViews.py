from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan
from django.template.loader import render_to_string
from django.http import JsonResponse



# Show Material
def crudShowMaterial(request):
    form = formMaterial()
    material = Material.objects.all()
    return render(request, 'siteWeb/crudMaterial/ajaxCrudMat.html', {'form': form, 'materials': material})


# Create Material
def ajaxCreateMaterial(request):
    if request.is_ajax and request.method == 'POST':
       form = formMaterial(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
       else:
           return JsonResponse({'error': True, 'errors': form.errors})
    #else:
        #form = formMaterial()
        #return render(request, 'siteWeb/crudMaterial/ajaxCrudMat.html', {'form': form})




# Update Material
def ajaxUpdateMaterial(request, id):
    id = request.GET.get('barcode', None)
    material_update = Material.objects.get(id=id)
    form = formMaterial(request.POST, request.FILES, instance=material_update)
    if form.is_valid():
       form.save()
       return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
    else:
        return JsonResponse({'error': True, 'errors': form.errors})



# Delete Type
class ajaxDeleteMaterial(View):
    def  get(self, request):
        id_material = request.GET.get('barcode', None)
        Material.objects.get(id = id_material).delete()
        data = {'deleted': True}
        return JsonResponse(data)