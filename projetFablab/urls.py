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
from django.contrib import admin
from django.urls import path
from siteWeb import views
from django.conf.urls.static import static
from django.conf import settings # new


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homepage, name="homepage"),
    path('addLoaner/', views.addLoaner, name= 'addLoaner'),
    path('addType/', views.addType, name='addType'),
    path('addMaterial/', views.addMateriel, name='addMaterial'),
    path('addLoan/', views.addLoan, name='addLoan'),
    path('addLoanMaterial', views.addLoanMaterial, name='addLoanMaterial'),
]

    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

