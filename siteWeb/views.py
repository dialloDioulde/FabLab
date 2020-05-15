import sys

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib import messages
from .forms import NewUserForm
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.mixins import LoginRequiredMixin
from siteWeb.models import LoanMaterial, Loaner, Loan, Material, Type, UserProfile
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan, formUnique, \
    EditProfileForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


# Homepage
def homepage(request):
    materials = Material.objects.all()
    search_term = ""

    if 'search' in request.GET:
        search_term = request.GET['search']
        materials = (materials.filter(name__icontains=search_term) | materials.filter(id__icontains=search_term))

        if search_term == "":
            search_term = "No match."

    paginator = Paginator(materials, 8)

    page = request.GET.get('page')

    materials = paginator.get_page(page)

    return render(request=request,
                  template_name="siteWeb/home.html",
                  context={"materials": materials, "search_term": search_term})


# ----------------------------------------------------------------------------------------------------------------------#

# Register
def register(request):
    # automatically, it's a GET request
    if not request.user.is_authenticated:
        return redirect("../../accounts/login")
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                # things are filled out like theyre supposed to
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"New Account Created:{username}")
                return redirect("homepage")
            else:
                for message in form.error_messages:
                    # print(form.error_messages[message])
                    messages.error(request, f"{message} : {form.error_messages[message]}")
        form = NewUserForm
        return render(request, "siteWeb/accounts/register.html", context={"form": form})


# Login
def login_request(request):
    if request.user.is_authenticated:
        return redirect("../../")
    else:
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
        return render(request, "siteWeb/accounts/login.html", {"form": form})


# Logout
# @login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")


# Show Profile
def showProfile(request):
    context = {'user': request.user}
    return render(request, "siteWeb/accounts/showProfile.html", context)


# Edit Profile
def editProfile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("showProfile")
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, "siteWeb/accounts/editProfile.html", context)


def change_password(request):
    if not request.user.is_authenticated:
        return redirect("../../accounts/login")
    else:
        if request.method == "POST":
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, f"Password Changed Successfully!")
                return redirect("homepage")
        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form}
            return render(request, "siteWeb/accounts/changePassword.html", args)


# ----------------------------------------------------------------------------------------------------------------------#
# Add Material
@login_required
def addMaterial(request):
    if not request.user.is_authenticated:
        return redirect("../../accounts/login")
    else:
        if request.method == 'POST':
            form = formMaterial(request.POST, request.FILES)
            if form.is_valid():
                type = form.cleaned_data.get('type')
                if type.material_type == 'unique':
                    type.unavailable = True
                    type.save()
                    from django.core.exceptions import ObjectDoesNotExist
                    try:
                        Material.objects.get(type=type)
                        messages.error(request, f"Existing unique type.")
                    except MultipleObjectsReturned:
                        return redirect(homepage)
                        messages.error(request, f"Error!")
                    except ObjectDoesNotExist:
                        form.save()
                        messages.success(request, f"New Material created")
                        return redirect("homepage")
                else:
                    form.save()
                    messages.success(request, f"New Material created")
                    return redirect("homepage")
        else:
            form = formMaterial()
        return render(request, 'siteWeb/addMaterial.html', {'form': form})


def updateMaterial(request, id):
    mat = Material.objects.get(id=id)
    form = formMaterial(instance=mat)

    if request.method == 'POST':
        form = formMaterial(request.POST, instance=mat)
        mat_type = Type.objects.get(id=mat.type.id)

        if mat_type.material_type == 'unique':
            mat_type.unavailable = False
            mat_type.save()

        if form.is_valid():
            type = form.cleaned_data.get('type')

            if type.material_type == 'unique':
                # mat_type.unavailable = False
                # mat_type.save()
                try:
                    Material.objects.get(type=type)
                    messages.error(request, f"Existing unique type.")
                except MultipleObjectsReturned:
                    messages.error(request, f"Error! Multiple Unique Materials.")
                    return redirect(homepage)
                except ObjectDoesNotExist:
                    type_unique = Type.objects.get(id=type.id)
                    type_unique.unavailable = True
                    type_unique.save()
                    form.save()
                    messages.success(request, f"New Material created")
                    return redirect("homepage")
            else:
                form.save()
                messages.success(request, f"New Material created")
                return redirect("homepage")

    context = {'form': form}
    return render(request, 'siteWeb/addMaterial.html', context)


# show single material
class MaterialDetailView(DetailView):
    model = Material
    template_name = "siteWeb/material.html"


# Delete Material
class DeleteCrudMaterial(View):
    def get(self, request):
        id_material = request.GET.get('id', None)
        Material.objects.get(id=id_material).delete()
        data = {'deleted': True}
        return JsonResponse(data)


# ----------------------------------------------------------------------------------------------------------------------#

# @login_required
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
            return redirect("/")

    else:
        loan_date = timezone.now()
        loan = Loan.objects.create(user=request.user, creation_date_loan=loan_date)
        loan.materials.add(loan_material)
        messages.info(request, "This item was added to your cart.")
        return redirect("/")


# @login_required
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


# @login_required
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


class EditLoanSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            active_loan = Loan.objects.get(user=self.request.user, ordered=False)

            active_loan_materials = active_loan.materials.all()
            active_loan_materials.update(ordered=False)
            for active_material in active_loan_materials:
                active_material.delete()
            active_loan.delete()
            loan = Loan.objects.get(id=kwargs['id'])
            loan.ordered = False
            loan.user = self.request.user

            loan_materials = loan.materials.all()
            loan_materials.update(ordered=False)

            loan.save()

            context = {
                'object': loan
            }
            return render(self.request, 'siteWeb/loan_summary.html', context)

        except ObjectDoesNotExist:
            loan = Loan.objects.get(id=kwargs['id'])
            loan.ordered = False
            loan.user = self.request.user

            loan_materials = loan.materials.all()
            loan_materials.update(ordered=False)

            loan.save()

            context = {
                'object': loan
            }
            return render(self.request, 'siteWeb/loan_summary.html', context)


class loan_form(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            loan = Loan.objects.get(user=self.request.user, ordered=False)
            form = formLoan(instance=loan or None)
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
                return redirect(homepage)
            else:
                messages.info(self.request, "Please fill in the required fields")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active loan")
        return redirect("loan-summary")


# ----------------------------------------------------------------------------------------------------------------------#
# -------------------------------LOANS----------------------------------------------------------------------------------#

# All Loans
def allLoan(request):
    loan_all = Loan.objects.filter(ordered=True)
    paginator = Paginator(loan_all, per_page=5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'siteWeb/all_Loan.html',
                  {'loan_all': page_obj.object_list, 'paginator': paginator, 'page_number': int(page_number)})


# Loan Not Returned
def notReturnedLoan(request):
    loan_not_ret = Loan.objects.filter(returned=False, ordered=True)
    paginator_2 = Paginator(loan_not_ret, per_page=5)
    page_number_2 = request.GET.get('page', 1)
    page_obj_2 = paginator_2.get_page(page_number_2)

    return render(request, 'siteWeb/loan_not_returned.html',
                  {'loan_not_ret': page_obj_2.object_list, 'paginator_2': paginator_2,
                   'page_number_2': int(page_number_2)})


# Loan Surpassed
def LoanSurpassed(request):
    now = timezone.now()
    loan_surpassed = Loan.objects.filter(returned=False, expected_return_date__lt=now).order_by('expected_return_date')
    paginator_3 = Paginator(loan_surpassed, per_page=5)
    page_number_3 = request.GET.get('page', 1)
    page_obj_3 = paginator_3.get_page(page_number_3)

    return render(request, 'siteWeb/loan_surpassed.html',
                  {'loan_surpassed': page_obj_3.object_list, 'paginator_3': paginator_3,
                   'page_number_3': int(page_number_3)})


# Show loan
def loan(request, id):
    loan = Loan.objects.get(id=id)
    loan_liste = loan.materials.all().order_by("-creation_date_loan_mat")
    paginator = Paginator(loan_liste, per_page=10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'siteWeb/loan.html',
                  {'loan_materials': page_obj.object_list, 'loan_loaner': loan, 'paginator': paginator,
                   'page_number': int(page_number)})


# Update loaner
def updateLoan(request, id):
    loan = Loan.objects.get(id=id)
    if not loan.returned:
        loan.returned = True
    else:
        loan.returned = False
    loan.return_date = timezone.now()
    loan.save()
    return redirect('allLoan')


# Delete Loan
class DeleteCrudLoan(View):
    def get(self, request):
        id_loan = request.GET.get('id', None)
        Loan.objects.get(id=id_loan).delete()
        data = {'deleted': True}
        return JsonResponse(data)
