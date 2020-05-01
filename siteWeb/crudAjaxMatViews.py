from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan
from django.template.loader import render_to_string
from django.http import JsonResponse



# Show Material
def indexView(request):
    form = formMaterial()
    material = Material.objects.all()
    return render(request, 'siteWeb/crudMaterial/ajaxCrudMat.html', {"form": form, "materials": material})




# Create Material
def CreateCrudMaterial(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = formMaterial(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


# Update Material
class UpdateCrudMaterial(View):
    def get(self, request):
        barcode = request.GET.get('barcode', None)
        material_name = request.GET.get('name', None)
        mat_type = request.GET.get('mat_type', None)

        obj = Material.objects.get(barcode = barcode)
        obj.name = material_name
        obj.type = mat_type

        obj.save()

        material = {'barcode': obj.barcode, 'name': obj.name, 'type': obj.mat_type}

        data = {
            'material': material
        }
        return JsonResponse(data)


# Delete Material
class DeleteCrudMaterial(View):
    def get(self, request):
        id_material = request.GET.get('barcode', None)
        Material.objects.get(barcode = id_material).delete()
        data = {'deleted': True}
        return JsonResponse(data)


