"""projetFablab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from siteWeb import views
from siteWeb.crudAjaxLoanerViews import LoanerView, CreateCrudLoaner, DeleteCrudLoaner, UpdateCrudLoaner
from siteWeb.crudAjaxTypeViews import TypeView, CreateCrudType, UpdateCrudType, DeleteCrudType
from siteWeb.crudAjaxMatViews import ajaxDeleteMaterial
from siteWeb import crudMaterialViews
from siteWeb import crudAjaxMatViews
from django.conf.urls.static import static
from django.conf import settings

from tinymce.widgets import TinyMCE

from siteWeb.views import(MaterialDetailView,LoanSummaryView,loan_form)


#----------------------------------------------------------------------------------------------------------------------#
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from siteWeb import views
from siteWeb.views import (
    MaterialDetailView,
    LoanSummaryView,
    loan_form,
)

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    path("", views.homepage, name="homepage"),

    # path('dashboard/', views.dashboard, name="dashboard"),
    path("material/<slug>/", MaterialDetailView.as_view(), name='material'),

    path("add-to-loan/<slug>", views.add_to_loan, name='add-to-loan'),
    path("remove-from-loan/<slug>", views.remove_from_loan, name='remove-from-loan'),
    path("add-one-material/<slug>", views.add_one_material, name='add-one-material'),
    path("remove-material-from-loan/<slug>", views.remove_single_item_from_loan, name='remove-material-from-loan'),
    path("loan-summary/", LoanSummaryView.as_view(), name="loan-summary"),
    path("loan/", loan_form.as_view(), name="loan"),

    path("accounts/register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("accounts/login/", views.login_request, name="login"),
    path("accounts/change-password/", views.change_password, name="change-password"),

    url('^', include('django.contrib.auth.urls')),

    path('addLoaner/', views.addLoaner, name='addLoaner'),
    path('addType/', views.addType, name='addType'),
    path('addMaterial/', views.addMaterial, name='addMaterial'),

    path('showLoaner', views.showLoaner, name='showLoaner'),
    path('showType', views.showType, name='showType'),
    path('showMaterial', views.showMaterial, name='showMaterial'),
    path('showLoan', views.showLoan, name='showLoan'),

    path('editLoaner/<int:id>',views.editLoaner, name='editLoaner'),
    path('updateLoaner/<int:id>',views.updateLoaner, name='updateLoaner'),

    path('editType/<int:id>',views.editType, name='editType'),
    path('updateType/<int:id>',views.updateType, name='updateType'),

    #path('deleteLoaner/<int:id>',views.deleteLoaner, name='deleteLoaner'),
    path('deleteType/<int:id>',views.deleteType, name='deleteType'),

    path('loan_id/<int:id>',views.loan, name='loan_id'),
    path('updateLoan/<int:id>',views.updateLoan, name='updateLoan'),
    path('deleteLoan/<int:id>', views.deleteLoan, name='deleteLoan'),

    #---------------------------- Ajax CRUD --------------------------------------------------------------------------#
    path('LoanerView', LoanerView.as_view(), name='LoanerView'),
    path('CreateCrudLoaner', CreateCrudLoaner.as_view(), name='CreateCrudLoaner'),
    path('DeleteCrudLoaner', DeleteCrudLoaner.as_view(), name='DeleteCrudLoaner'),
    path('UpdateCrudLoaner', UpdateCrudLoaner.as_view(), name='UpdateCrudLoaner'),


    path('TypeView', TypeView.as_view(), name='TypeView'),
    path('CreateCrudType', CreateCrudType.as_view(), name='CreateCrudType'),
    path('UpdateCrudType', UpdateCrudType.as_view(), name='UpdateCrudType'),
    path('DeleteCrudType', DeleteCrudType.as_view(), name='DeleteCrudType'),


    path('ajaxShowMat', crudAjaxMatViews.crudShowMaterial, name='ajaxShowMat'),
    path('ajaxUpdateMat/<int:id>', crudAjaxMatViews.ajaxUpdateMaterial, name='ajaxUpdateMat'),
    path('ajaxCreateMat', crudAjaxMatViews.ajaxCreateMaterial , name='ajaxCreateMat'),
    path('ajaxDeleteMat', ajaxDeleteMaterial.as_view(), name='ajaxDeleteMat'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

