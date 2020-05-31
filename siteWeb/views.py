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
from siteWeb.forms import formLoan, formType, formLoaner, formLoanMaterial, formMaterial, formLoan, EditProfileForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


# Homepage
def homepage(request):
    """
    Homepage, where materials are displayed. A search bar is placed for the user to be able to search for materials.
    \nWhen more than 8 materials are in the DB, then a pagination is placed.

    :param request: This request object contains information set by entities present before a view method.
    :return: Webpage *home.html*, displaying list of *materials*.

    """
    materials = Material.objects.all()
    search_term = ""

    #search bar: show material after search based on name and barcode
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


# ----------------------------------------------------------------------------------------------------------------------#

# Register
def register(request):
    """
    **Context**
    \nRegister a new Staff Member. Only the Administrator has the possibility to create a new Account.

    :param request:  This request object contains information set by entities present before a view method.
    :return: If the user is not the superuser, then there is a redirection to /login.
        Elsewise, the redirection brings you to /homepage and the form is saved as a parameter sent as a context.
    """

    # automatically, it's a GET request
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("../../accounts/login")
    else:
        if request.method == "POST":
            form = NewUserForm(request.POST)
            if form.is_valid():
                # things are filled out like theyre supposed to
                username = form.cleaned_data.get('username')
                messages.success(request, f"New Account Created:{username}")
                return redirect("homepage")
            else:
                for message in form.error_messages:
                    messages.error(request, f"{message} : {form.error_messages[message]}")
        form = NewUserForm
        return render(request, "siteWeb/accounts/register.html", context={"form": form})


# Login
def login_request(request):
    """
        **Context**
        \nA user that already has an account (previously create by the Admin OR the actual Admin himself) can login.
        \nDifferent type of functionalities are possible once the user is logged in.

        :param request:  This request object contains information set by entities present before a view method.
        :return: If the user is not authenaticated, then there is a redirection to /login.
            Elsewise, the redirection brings you to /homepage and the form is saved as a parameter sent as a context.
    """
    if request.user.is_authenticated:
        return redirect("../../")
    else:
        if request.method == "POST":
            #automatically generated authentication form
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
@login_required
def logout_request(request):
    """
        **Context**
        \nA user that has logged in prior to this step, can also logout.

        :param request:  This request object contains information set by entities present before a view method.
        :return: Once the log out is successful, the redirection brings you to homepage.
    """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")


# Show Profile
@login_required
def showProfile(request):
    """
    **Context**
    \nA page where the personal authenticated user's information is shown, such as: username, first and last name, email.

    :param request: This request object contains information set by entities present before a view method.
    :return: redirection to the /showProfile page.
    """
    context = {'user': request.user}
    return render(request, "siteWeb/accounts/showProfile.html", context)


# Edit Profile
@login_required
def editProfile(request):
    """
    **Context**
    \nModifying the authenticated user's information, such as changing the username, first and last name or email.

    :param request: This request object contains information set by entities present before a view method.
    :return: If the form is valid, the redirection brings you to the personal page of the authenticated user.
    """

    if request.method == "POST":
        #show form to Edit Profile with instance set to the information of authenticated
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("showProfile")
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, "siteWeb/accounts/editProfile.html", context)


@login_required
def change_password(request):
    """
    **Context**
    \nOnce the user is authenticated, he has the possibility to change the password, by putting once the old password
    and twice the new one. Once the change is saved, the user will be able to authenticate using the new password.

    :param request: This request object contains information set by entities present before a view method.
    :return: If the change is successful, the redirection brings you to the homepage.
    """
    if not request.user.is_authenticated:
        return redirect("../../accounts/login")
    else:
        if request.method == "POST":
            #form set set as a Password Change Form which the infomation of the user authenticated
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, f"Password Changed Successfully!")
                return redirect("showProfile")
            else:
                messages.info(request, f"Password Unmatch! Try again.")
                return redirect("change-password")
        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form}
            return render(request, "siteWeb/accounts/changePassword.html", args)


# ----------------------------------------------------------------------------------------------------------------------#
# Add Material
@login_required
def addMaterial(request):
    """
    **Context**
    \nAdding a new Material, requires to fill a form with different fields such as name, barcode and choosing a type.
    \nIf the chosen type of the material is a UNIQUE one, the type gets removed form the dropdown where the user
    is able to choose between the types available (ONE and ONLY ONE material can be created out of a UNIQUE Type).
    \nIf the type is GENERIC, the number of materials created is not taken into consideration.

    :param request: This request object contains information set by entities present before a view method.
    :return: If the Material is added successfully, then the redirection brings you to the homepage.
    """
    if request.method == 'POST':
        form = formMaterial(request.POST, request.FILES)
        if form.is_valid():
            type = form.cleaned_data.get('type')

            #check if type is unique
            if type.material_type == 'unique':
                #if so, set type as unavailable so it won't be available to create another material with the same type
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

@login_required
def updateMaterial(request, id):
    """
    **Context**
    \nThe modification of an existing material is possible. The edit of the name, barcode and also Type can be done during
    this step. Whenever a Type is changed, there is a check to see if the old type or the new is a UNIQUE one.
    If either of them is UNIQUE, the (respective) old or new type gets added or removed from the list of available types to choose from.

    :param request: This request object contains information set by entities present before a view method.
    :param id: ID of the material that is about to be modified.
    :return: Updates material with specified ID and redirects to homepage.
    """
    mat = Material.objects.get(id=id)
    form = formMaterial(instance=mat)

    if request.method == 'POST':
        form = formMaterial(request.POST,request.FILES,instance=mat)
        mat_type = Type.objects.get(id=mat.type.id)

        if mat_type.material_type == 'unique':
            mat_type.unavailable = False
            mat_type.save()

        if form.is_valid():
            type = form.cleaned_data.get('type')

            if type.material_type == 'unique':
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
                    messages.success(request, f"Material Edited Successfully!")
                    return redirect("homepage")
            else:
                form.save()
                messages.success(request, f"Material Edited Successfully!")
                return redirect("homepage")

    context = {'form': form}
    return render(request, 'siteWeb/addMaterial.html', context)


# show single material
# @login_required
class MaterialDetailView(DetailView):
    """
    **Context**
    \nViewing the information of a specific material, such as name, barcode, type, description of type and image.
    \nWhen logged in, other functionalities are added, such as buttons to edit material, add/remove to loan.
    """
    model = Material
    template_name = "siteWeb/material.html"


# Delete Material
# @login_required
class DeleteCrudMaterial(View):
    """
    **Context**
    \nRemoving a material from the DB. Delete the specific object.
    """
    def get(self, request):
        id_material = request.GET.get('id', None)
        Material.objects.get(id=id_material).delete()
        data = {'deleted': True}
        return JsonResponse(data)


# ----------------------------------------------------------------------------------------------------------------------#

@login_required
def add_to_loan(request, slug):
    """
    **Context**
    \nA material can be added to the Loan. Whenever this step is done, the material added is going to be visible to the
    card in the navigation bar on the top right.

    :param request: This request object contains information set by entities present before a view method.
    :param slug: Refers to the Material; it's an identification to a specific material.
    :return: Whenever the material is added to an active Loan, then a redirection to homepage takes place, leaving space
        to the user to add more materials to the loan.
    """
    material = get_object_or_404(Material, slug=slug)
    loan_material, created = LoanMaterial.objects.get_or_create(material=material, user=request.user, ordered=False)
    material_query = Loan.objects.filter(user=request.user, ordered=False)
    if material_query.exists():
        loan = material_query[0]
        # check if the order item is in the order
        if loan.materials.filter(material__slug=material.slug).exists():
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


@login_required
def add_one_material(request, slug):
    """
    **Context*
    \nModify the quantity of the material. Add it by one, whenever the button is pressed.

    :param request: This request object contains information set by entities present before a view method.
    :param slug: Refers to the Material; it's an identification to a specific material.
    :return: If the augmentation of the quantity is successful, the redirection brings you to the same page: /loan-summary,
        where all the materials and the corresponding quantities added to the active order are.
    """
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
    """
    **Context**
    \nRemove an existing material from Loan (that was added to it to previous steps).

    :param request: This request object contains information set by entities present before a view method.
    :param slug: Refers to the Material; it's an identification to a specific material.
    :return: If the removal of the material from the loan is successful, the redirection brings you to the same page: /loan-summary,
        where the list of the materials that are left with the corresponding quantities added to the active order are shown.
    """
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


# @login_required
class LoanSummaryView(LoginRequiredMixin, View):
    """
            **Context**
            \nWhen a user is authenaticated, he can have ONE and ONE ONLY active loan. Whenever the materials are added,
            they are visible to the /loan-summary page in a form of a list with the corresponding quantity for each material
            that is going to the loan.

            :return: Shows the list of materials at /loan-summary.
    """
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

# @login_required
class EditLoanSummaryView(LoginRequiredMixin, View):
    """
           **Context**
           \nModification of the Loan. Whenever a loan is saved, a new object is placed into the DB and another one is automatically created.
           Since only ONE loan can be opened and be active for the user to make modifications, it's necessary to re-activate
           an already-saved Loan.
           \nThe list of the materials is added to the Loan and it's accessible at /loan-summary.
           \nThe quantities and the materials themselves can be modified. So can the Loaner and the Returned Date.

           :return: /loan-summary with the list of materials existing on the desired to be modified loan
    """
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
    """
           **Context**
           \nForm to add to the active Loan, the Loaner and the Expected return Date.
           \nIf the values already exist (update case), than the object gets those values by setting instance to the loan.
           If not, the Values are empty and needed to be filled.

           :return: Whenever the last values (loaner and expected return date) are added to the Loan, a Loan object is saved
               into the DB. Redirection brings the user to homepage if saving is successful.
    """
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

                messages.success(self.request, f"Loan saved successfully")
                return redirect(homepage)
            else:
                messages.info(self.request, "Please fill in the required fields")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active loan")
        return redirect("loan-summary")


# ----------------------------------------------------------------------------------------------------------------------#
# -------------------------------LOANS----------------------------------------------------------------------------------#

# All Loans
@login_required
def allLoan(request):
    """
    **Context**
    \nShow all Loans that were ever saved.

    :param request:  This request object contains information set by entities present before a view method.
    :return: Table of all the loan objects ever created, shown at /allLoan.
    """
    loan_all = Loan.objects.filter(ordered=True)
    paginator = Paginator(loan_all, per_page=5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'siteWeb/all_Loan.html',
                  {'loan_all': page_obj.object_list, 'paginator': paginator, 'page_number': int(page_number)})


# Loan Not Returned
@login_required
def notReturnedLoan(request):
    """
        **Context**
        \nShow Loans that are considered as *Not returned*, which means that the Loaner did not bring back the materials
        to FabLab physically. Once they do, the Loan that corresponds to this Loaner and those specific materials, is
        registered as returned.

        :param request:  This request object contains information set by entities present before a view method.
        :return: Table of not returned loan objects, shown at /NotReturnedLoan.
    """
    loan_not_ret = Loan.objects.filter(returned=False, ordered=True)
    paginator_2 = Paginator(loan_not_ret, per_page=5)
    page_number_2 = request.GET.get('page', 1)
    page_obj_2 = paginator_2.get_page(page_number_2)

    return render(request, 'siteWeb/loan_not_returned.html',
                  {'loan_not_ret': page_obj_2.object_list, 'paginator_2': paginator_2,
                   'page_number_2': int(page_number_2)})


# Loan Surpassed
@login_required
def LoanSurpassed(request):
    """
        **Context**
        \nShow Loans that are whose return date has surpassed and yet they are not returned, which means that the Loaner
        did not bring back the materials in time to FabLab physically. Once they do, the Loan that corresponds to this
        Loaner and those specific materials, is registered as returned.

        :param request: This request object contains information set by entities present before a view method.
        :return: Table of not returned whose expected return date has surpassed loan objects, shown at /SurpassedLoan.
    """
    now = timezone.now()
    loan_surpassed = Loan.objects.filter(returned=False, expected_return_date__lt=now).order_by('expected_return_date')
    paginator_3 = Paginator(loan_surpassed, per_page=5)
    page_number_3 = request.GET.get('page', 1)
    page_obj_3 = paginator_3.get_page(page_number_3)

    return render(request, 'siteWeb/loan_surpassed.html',
                  {'loan_surpassed': page_obj_3.object_list, 'paginator_3': paginator_3,
                   'page_number_3': int(page_number_3)})


# Show loan
@login_required
def loan(request, id):
    """
    **Context**
    \nShow details of specific loan, such as: name of Loaner, expected return date, list of materials etc.

    :param request:  This request object contains information set by entities present before a view method.
    :param id: ID that corresponds to specific Loan.
    :return: A page with details of specific loan.
    """
    loan = Loan.objects.get(id=id)
    loan_liste = loan.materials.all().order_by("creation_date_loan_mat")
    paginator = Paginator(loan_liste, per_page=10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'siteWeb/loan.html',
                  {'loan_materials': page_obj.object_list, 'loan_loaner': loan, 'paginator': paginator,
                   'page_number': int(page_number)})


# Update loaner
@login_required
def updateLoan(request, id):
    """
    **Context**
    \nMark Loan as Returned (True) and also the date when it was returned. If already TRUE, mark it as (False).

    :param request:  This request object contains information set by entities present before a view method.
    :param id: ID that corresponds to specific Loan.
    :return: Redirect to the same page of details of a specific loan whose Return value whe just changed.
    """
    loan = Loan.objects.get(id=id)
    if not loan.returned:
        loan.returned = True
        loan.return_date = timezone.now()
    else:
        loan.returned = False
        loan.return_date = None
    loan.save()
    return redirect("loan_id", id=id)


# Delete Loan
class DeleteCrudLoan(View):
    """
    **Context**
    \nDelete a Loan from the DB.
    """
    def get(self, request):
        id_loan = request.GET.get('id', None)
        Loan.objects.get(id=id_loan).delete()
        data = {'deleted': True}
        return JsonResponse(data)
