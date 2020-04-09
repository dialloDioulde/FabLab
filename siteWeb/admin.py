from django.contrib import admin
from tinymce import TinyMCE

# Register your models here.


from .models import Type, Material, Loaner, LoanMaterial, Loan

admin.site.register(Type)
admin.site.register(Material)
admin.site.register(Loaner)
admin.site.register(Loan)
admin.site.register(LoanMaterial)