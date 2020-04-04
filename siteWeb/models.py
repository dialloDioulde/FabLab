from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Loaner(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    establishment = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name + " " + self.first_name


class Type(models.Model):
    TYPE_GENERIC = 'generic'
    TYPE_UNIQUE = 'unique'

    TYPE_CHOICES = (
        (TYPE_GENERIC, 'generic'),
        (TYPE_UNIQUE, 'unique'),
    )
    material_type = models.CharField(max_length=250, choices=TYPE_CHOICES, default=TYPE_GENERIC)
    name_type = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    creation_date_type = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}".format(self.name_type)


class Material(models.Model):
    name = models.CharField(max_length=250)
    barcode = models.IntegerField(blank=False, primary_key=True)
    creation_date_mat = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    material_picture = models.ImageField(blank=True, upload_to='media/', default='None/no-img.jpg', null=True)

    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (barcode:  " + str(self.barcode) + ")"

    def get_absolute_url(self):
        return reverse("main:material", kwargs={
            'slug': self.slug
        })

    def get_add_to_loan_url(self):
        return reverse("main:add-to-loan", kwargs={
            'slug': self.slug
        })

    def get_remove_from_loan_url(self):
        return reverse("main:remove-from-loan", kwargs={
            'slug': self.slug
        })


class LoanMaterial(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    quantity = models.IntegerField(blank=False, default=1)
    creation_date_loan_mat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.quantity) + " of " + self.material.name


class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    creation_date_loan = models.DateTimeField(default=timezone.now)
    expected_return_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(null=True)

    loaner = models.ForeignKey(Loaner, on_delete=models.CASCADE, blank=False, null=True)
    materials = models.ManyToManyField(LoanMaterial)

    def __str__(self):
        return "{0}".format(self.pk)