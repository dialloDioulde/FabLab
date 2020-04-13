from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.http import *
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Material, Type
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import NewUserForm
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan


# Homepace
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


def dashboard(request):
    return render(request, "siteWeb/dashboard.html")


# show single material
class MaterialDetailView(DetailView):
    model = Material
    template_name = "siteWeb/material.html"


def register(request):
    # automatically, it's a GET request

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # things are filled out like theyre supposed to
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created:{username}")
            # login(request, user)
            # messages.info(request, f"Logged in as  {username}")
            return redirect("homepage")
        else:
            for message in form.error_messages:
                # print(form.error_messages[message])
                messages.error(request, f"{message} : {form.error_messages[message]}")
    form = NewUserForm
    return render(request,
                  "siteWeb/register.html",
                  context={"form": form}
                  )


# @login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")


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
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request,
                  "siteWeb/login.html",
                  {"form": form}
                  )


# Borrower registration
# @login_required # You will need to be logged in
def addLoaner(request):
    sauvegarde = False
    if request.method == 'POST':
        form = formLoaner(request.POST)
        form.save()
        form = formLoaner()
        messages.success(request, f"New Loaner created")
        return redirect("homepage")
        sauvegarde = True
    else:
        form = formLoaner()
    return render(request, 'siteWeb/addLoaner.html', {'form': form})


# Add Type
# @login_required
def addType(request):
    sauvegarde = False
    if request.method == 'POST':
        form = formType(request.POST)
        form.save()
        form = formType()
        messages.success(request, f"New Type created")
        return redirect("homepage")
        sauvegarde = True
    else:
        form = formType()
    return render(request, 'siteWeb/addType.html', {'form': form, 'sauvegarde': sauvegarde})


# Add Material
# @login_required
def addMaterial(request):
    sauvegarde = False
    if request.method == 'POST':
<<<<<<< Updated upstream
        form = formMaterial(request.POST, request.FILES)
=======
        form = formMaterial(request.POST or None, request.FILES)
>>>>>>> Stashed changes
        if form.is_valid():
            type = form.cleaned_data.get('type')
            if type.material_type == 'unique':
                from django.core.exceptions import ObjectDoesNotExist
                try:
                    Material.objects.get(type=type)
                    messages.error(request, f"Existing unique type.")
                except ObjectDoesNotExist:
                    form.save()
                    form = formMaterial()
                    messages.success(request, f"New Material created")
                    return redirect("homepage")
                    sauvegarde = True
            else:
                form.save()
                form = formMaterial()
                messages.success(request, f"New Material created")
                return redirect("homepage")
                sauvegarde = True
    else:
        form = formMaterial()
    return render(request, 'siteWeb/addMaterial.html', {'form': form, 'sauvegarde': sauvegarde})


# Show Loaner
def showLoaner(request):
    loaner_liste = Loaner.objects.all()
    return render(request, 'siteWeb/showLoaner.html', {'loaners': loaner_liste})


# Show Type
def showType(request):
    type_liste = Type.objects.all()
    return render(request, 'siteWeb/showType.html', {'types': type_liste})


# Show Material
def showMaterial(request):
    material_liste = Material.objects.all()
    return render(request, 'siteWeb/showMaterial.html', {'materials': material_liste})


# Edit Loaner
def editLoaner(request, id):
    loaner_edit = Loaner.objects.get(id=id)
    return render(request, 'siteWeb/editLoaner.html', {'loaner_edit': loaner_edit})


# Update Loaner
def updateLoaner(request, id):
    loaner_update = Loaner.objects.get(id=id)
    form = formLoaner(request.POST, instance=loaner_update)
    if form.is_valid():
        form.save()
        messages.success(request, f"Loaner Updated successfully")
        return redirect(showLoaner)
    messages.error(request, f"Loaner not updated! Try again.")
    return render(request, 'siteWeb/editLoaner.html', {'user_update': form})


# Edit Type
def editType(request, id):
    type_edit = Type.objects.get(id=id)
    return render(request, 'siteWeb/editType.html', {'type_edit': type_edit})


# Update Type
def updateType(request, id):
    type_update = Type.objects.get(id=id)
    form = formType(request.POST, instance=type_update)
    if form.is_valid():
        form.save()
        messages.success(request, f"Type Updated successfully")
        return redirect(showType)
    messages.error(request, f"Type not updated! Try again.")
    return render(request, 'siteWeb/editType.html', {'type_update': form})


@login_required
def add_to_loan(request, slug):
    material = get_object_or_404(Material, slug=slug)
    loan_material, created = LoanMaterial.objects.get_or_create(material=material, user=request.user, ordered=False)
    material_query = Loan.objects.filter(user=request.user, ordered=False)
    if material_query.exists():
        loan = material_query[0]
        # check if the order item is in the order
        if loan.materials.filter(material__slug=material.slug).exists():
            # loan_material.quantity += 1
            loan_material.save()
            messages.info(request, "Material Already exists in Loan.")
            return redirect("/")
        else:
            loan.materials.add(loan_material)
            messages.info(request, loan_material)
            return redirect("material", slug=slug)

    else:
        loan_date = timezone.now()
        loan = Loan.objects.create(user=request.user, creation_date_loan=loan_date)
        loan.materials.add(loan_material)
        messages.info(request, "This item was added to your cart.")
        return redirect("material", slug=slug)


@login_required
def add_one_material(request, slug):
    material = get_object_or_404(Material, slug=slug)
    loan_material, created = LoanMaterial.objects.get_or_create(material=material, user=request.user, ordered=False)
    material_query = Loan.objects.filter(user=request.user, ordered=False)
    if material_query.exists():
        loan = material_query[0]
        # check if the order item is in the order
        if loan.materials.filter(material__slug=material.slug).exists():
            loan_material.quantity += 1
            loan_material.save()
            messages.info(request, "+1 Material Added.")
            return redirect("loan-summary")
        else:
            loan.materials.add(loan_material)
            messages.info(request, loan_material)
            return redirect("material", slug=slug)

    else:
        loan_date = timezone.now()
        loan = Loan.objects.create(user=request.user, creation_date_loan=loan_date)
        loan.materials.add(loan_material)
        messages.info(request, "This item was added to your cart.")
        return redirect("material", slug=slug)


@login_required
def remove_from_loan(request, slug):
    material = get_object_or_404(Material, slug=slug)
    material_query = Loan.objects.filter(user=request.user, ordered=False)

    if material_query.exists():
        loan = material_query[0]
        # check if the order item is in the order
        if loan.materials.filter(material__slug=material.slug).exists():
            loan_material = LoanMaterial.objects.filter(material=material, user=request.user, ordered=False)[0]
            loan.materials.remove(loan_material)
            loan_material.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("loan-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("material", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("material", slug=slug)


@login_required
def remove_single_item_from_loan(request, slug):
    material = get_object_or_404(Material, slug=slug)
    material_query = Loan.objects.filter(user=request.user, ordered=False)
    if material_query.exists():
        loan = material_query[0]
        # check if the order item is in the order
        if loan.materials.filter(material__slug=material.slug).exists():
            loan_material = LoanMaterial.objects.filter(
                material=material,
                user=request.user,
                ordered=False)[0]
            if loan_material.quantity > 1:
                loan_material.quantity -= 1
                loan_material.save()
            else:
                loan.materials.remove(loan_material)
            messages.info(request, "This item quantity was updated.")
            return redirect("loan-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("material", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("material", slug=slug)


class LoanSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            loan = Loan.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': loan
            }
            return render(self.request, 'siteWeb/loan_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


class loan_form(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            form = formLoan()
            context = {
                'formLoan': form,
            }
            return render(self.request, 'siteWeb/loanForm.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = formLoan(self.request.POST or None)
        loan = Loan.objects.get(user=self.request.user, ordered=False)
        try:
            if form.is_valid():
                expected_return = form.cleaned_data.get('expected_return_date')

                loan.ordered = True
                loan.save()

                loan.expected_return_date = expected_return
                loan.save()

                loan.loaner = form.cleaned_data.get('loaner')
                loan.save()

                loan.user = self.request.user
                loan.save()

                loan_materials = loan.materials.all()
                loan_materials.update(ordered=True)
                for material in loan_materials:
                    material.save()

                messages.success(self.request, f" Loan saved successfully")
                return redirect("homepage")
            else:
                messages.info(self.request, "Please fill in the required fields")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active loan")
        return redirect("loan-summary")
