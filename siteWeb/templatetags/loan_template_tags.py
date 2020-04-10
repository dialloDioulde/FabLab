from django import template
from siteWeb.models import Loan

register = template.Library()

@register.filter
def loan_materials_count(user):
    if user.is_authenticated:
        qs = Loan.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].materials.count()
    return 0