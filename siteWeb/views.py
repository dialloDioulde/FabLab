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

from siteWeb.models import LoanMaterial,Loaner,Loan,Material,Type,UserProfile
from siteWeb.forms import formLoan,formType,formLoaner,formLoanMaterial,formMaterial

# Welcome Page d'Acceuil
def welcome(request):
    return render(request,'siteWeb/base.html')



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