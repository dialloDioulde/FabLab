from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Loaner
from django.views.generic import TemplateView, View, DeleteView
from django.core import serializers
from django.http import JsonResponse
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan


# Show Loaner
class LoanerView(TemplateView):
    template_name = 'siteWeb/loaner/ajaxCrudLoaner.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loaners'] = Loaner.objects.all()
        return context


# Create Loaner
class CreateCrudLoaner(View):
    def get(self, request):
        last_name = request.GET.get('last_name', None)
        first_name = request.GET.get('first_name', None)
        email = request.GET.get('email', None)
        establishment = request.GET.get('establishment', None)

        obj = Loaner.objects.create(last_name=last_name, first_name=first_name, email=email,
                                    establishment=establishment)

        loaner = {'id': obj.id, 'last_name': obj.last_name, 'first_name': obj.first_name, 'email': obj.email,
                  'establishment': obj.establishment}

        data = {
            'loaner': loaner
        }
        return JsonResponse(data)


# Delete Loaner
class DeleteCrudLoaner(View):
    def get(self, request):
        id_loaner = request.GET.get('id', None)
        Loaner.objects.get(id=id_loaner).delete()
        data = {'deleted': True}
        return JsonResponse(data)


# Update Loaner
class UpdateCrudLoaner(View):

    def get(self, request):
        id_loaner = request.GET.get('id_loaner', None)

    def  get(self, request):
        id = request.GET.get('id_loaner', None)

        last_name_e = request.GET.get('last_name', None)
        first_name_e = request.GET.get('first_name', None)
        email_e = request.GET.get('email', None)
        establishment_e = request.GET.get('establishment', None)


        obj = Loaner.objects.get(id=id_loaner)

        obj = Loaner.objects.get(id = id)

        obj.last_name = last_name_e
        obj.first_name = first_name_e
        obj.email = email_e
        obj.establishment = establishment_e

        obj.save()


        loaner = {'id': obj.id_loaner, 'last_name': obj.last_name, 'first_name': obj.first_name, 'email': obj.email,
                  'establishment': obj.establishment}

        loaner = {'id':obj.id,'last_name':obj.last_name,'first_name':obj.first_name,'email':obj.email, 'establishment':obj.establishment}



        data = {
            'loaner': loaner
        }
        return JsonResponse(data)


