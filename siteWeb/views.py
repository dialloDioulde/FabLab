from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import *
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Material, Type
from django.core.paginator import Paginator

from siteWeb.models import LoanMaterial,Loaner,Loan,Material,Type,UserProfile
from siteWeb.forms import formLoan,formType,formLoaner,formLoanMaterial,formMaterial

# Create your views here.
def homepage(request):
    materials = Material.objects.all()

# Welcome Page d'Acceuil
def welcome(request):
    return render(request,'siteWeb/base.html')

#Homepace
def homepage(request):
    materials = Material.objects.all()
    search_term = ""

    if 'search' in request.GET:
        search_term = request.GET['search']
        materials = (materials.filter(name__icontains=search_term) | materials.filter(barcode__icontains=search_term))

        if search_term == "":
            search_term = "No match."

    paginator = Paginator(materials, 8)

    page = request.GET.get('page')

    materials = paginator.get_page(page)

    return render(request=request,
                  template_name="siteWeb/home.html",
                  context={"materials": materials, "search_term": search_term})



# Borrower registration
# @login_required # You will need to be logged in
def addLoaner(request):
    if request.method == 'POST':
        form = formLoaner(request.POST)
        form.save()
        print(form.instance)
    else:
        form = formLoaner()
    return render(request, 'siteWeb/addLoaner.html', {'form': form})