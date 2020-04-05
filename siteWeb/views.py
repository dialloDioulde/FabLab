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
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


from siteWeb.models import LoanMaterial,Loaner,Loan,Material,Type,UserProfile
from siteWeb.forms import formLoan,formType,formLoaner,formLoanMaterial,formMaterial

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

def register(request):
    # automatically, it's a GET request

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # things are filled out like theyre supposed to
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created:{username}")
            login(request, user)
            messages.info(request, f"Logged in as  {username}")
            return redirect("main:homepage")
        else:
            for message in form.error_messages:
                # print(form.error_messages[message])
                messages.error(request, f"{message} : {form.error_messages[message]}")
    form = NewUserForm
    return render(request,
                  "main/register.html",
                  context={"form": form}
                  )


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Logged in as  {username}")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request,
                  "main/login.html",
                  {"form": form}
                  )

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