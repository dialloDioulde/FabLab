from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from projetFablab.utils import unique_slug_generator


# Create your models here.
class UserProfile(models.Model):
    """
    **Context**

    The table *UserProfile* allows the user who's logged in to be considered as the only active user for
    his account.\n
    This way, the differences between accounts can be done and ONE and ONLY ONE user corresponds to an Account.\n
    Useful to differentiate the Loans created from different accounts.

    :param user: Specifies a ONE to ONE Field with the Authenticated user, making it possible to create the unique
                connection between the authenticated user and the account.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Loaner(models.Model):
    """
        **Context**
        A Loaner is someone who loans materials from the FabMSTIC.\n
        His information is saved and attached to the Loan, as the temporary owner of the loaned materials.

        :param last_name: Loaner's Last Name
        :param first_name: Loaner's First Name
        :param email: Loaner's Email, needed for further updates, such as contact
        :param establishment: Loaner's Establishment, such as IMAG, UGA etc. Keeping track where does the Loaner come
            from, wanting all the Loaners to be part of the University as a Professor, Researcher, Student etc.
        :param creation_date: Keep track of when the Loaner was created, in case any further modification need to be done.
    """
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    establishment = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.last_name + " " + self.first_name


class Type(models.Model):

    """
        **Context**
        \n A type usually represents a model or a brand, which can be considered as Generic or Unique, based on the number of
        materials that the FabMSTIC owns.
        A Type is created to serve to the creation on Materials.

        :param TYPE_UNIQUE: Represents a type, which once created, corresponds to ONE and ONLY ONE Material.
            In other words, FabLab owns only ONE Material of this SPECIFIC TYPE.
        :param TYPE_GENERIC: Represents a type, which once created, can correspond to multiple Materials.
            FabLab owns different type of Materials of the same model or brand.
        :param material_type: d
        :param name_type: Name of the Type.
        :param description: Brief description of the Type.
        :param creation_date_type: Date when the Type was Created.
        :param unavaiable: Boolean Value to make it possible to keep track if the Unique Values are used already or not
            (if a Material is created by a specific Unique Type already or Not).
    """
    TYPE_GENERIC = 'generic'
    TYPE_UNIQUE = 'unique'

    TYPE_CHOICES = (
        (TYPE_GENERIC, 'generic'),
        (TYPE_UNIQUE, 'unique'),
    )
    material_type = models.CharField(max_length=250, choices=TYPE_CHOICES, default=TYPE_GENERIC)
    name_type = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    creation_date_type = models.DateTimeField(auto_now_add=True)
    unavailable = models.BooleanField(default=False)

    def __str__(self):
        return self.name_type + " - " + self.material_type


class Material(models.Model):
    """
        **Context**
        \n A Material represents a physical object. It can be either Unique, which means it only exists once in the FabLab inventory
        (and it corresponds to a Unique Type), or it can be Generic, meaning that FabLab owns multiple of this physical object
        (and it corresponds to a Generic Type).

        :param name: Name of Material
        :param barcode: A Material has it's unique identification code.
        :param creation_date_mat: The date when this material was created.
        :param material_picture: An image added (if desired).
        :param type: A FK to Type, corresponding to the model/brand of the material created.
        :param slug: Unique Name for the Material, used to generate the absolute url
    """
    name = models.CharField(max_length=250)
    barcode = models.CharField(max_length=50)
    creation_date_mat = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    material_picture = models.ImageField(blank=True, upload_to='media/', default='None/no-img.jpg', null=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " (id:  " + str(self.id) + ")"

    def get_absolute_url(self):
        """
            Calculate the canonical URL for an object. Used to visualize a single material.

            :return: /material/<slug>
        """
        return reverse("material", kwargs={
            'slug': self.slug
        })

    def get_add_to_loan_url(self):
        """
            Add a specific Material Loan.

           :return:  /add-to-loan/<slug>
        """
        return reverse("add-to-loan", kwargs={
            'slug': self.slug
        })

    def get_remove_from_loan_url(self):
        """
          Remove a specific Material from Loan.

          :return: /remove-from-loan/<slug>
        """
        return reverse("remove-from-loan", kwargs={
            'slug': self.slug
        })


def slug_generator(sender, instance, *args, **kwargs):
    """
        Generation of a unique slug, based on the parameter instance.

        :param sender: Class where the automatic generation of unique slugs is going to be

        :return:
            unique slug for object created by Table specified in sender
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Material)


class LoanMaterial(models.Model):
    """
        **Context**
        \n Middle step that saves the quantity for each material whenever a Loan is being placed.

        :param user: corresponds as a FK to the Table *UserProfile*
        :param ordered: Boolean Value saving if the LoanMaterial is active or not. If active(ordered=False): Materials are
            temporally added to a LoanMaterial. Possibility to modify the list of materials and their quantity.
            If inactive(ordered=True): The previous object(s) of LoanMaterial are saved into the DB,
            leaving place to (an)other LoanMaterial object to be created.
        :param material: FK to a material.
        :param quantity: Quantity corresponding to Material (specified as a FK).
        :param creation_date_loan_mat: Creation date of LoanMaterial

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    quantity = models.IntegerField(blank=False, default=1)
    creation_date_loan_mat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.quantity) + " " + self.material.name


class Loan(models.Model):
    """
        **Context**
        \n A user can add materials to the loan, add a loaner and an expected return date and save it as an Object called Loan.

        :param user: ONE and only ONE Loan can be connected to the user authenticated.
        :param ordered: ONE and only ONE Loan connected to the user authenticated can be FALSE, which means that there is
            ONLY ONE ACTIVE Loan object being created.
        :param returned: The Material(s) of the Loan were returned physically to the FabLab (True) or not (False).
        :param loaner: The person who is taking the material(s) with them.
        :param materials: List of materials and their quantity that the Loaner is borrowing from FabLab.
            Specified as a Many to Many field, which means that multiple materials can be added to the same Loan.
        :param expected_return_date: The limit of time that is given to the Loaner to return the loaned material(s).
        :param returned_date: Actual Date when the Loaner returned physically the material(s).

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    returned = models.BooleanField(default=False)

    creation_date_loan = models.DateTimeField(default=timezone.now)
    expected_return_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(null=True)

    loaner = models.ForeignKey(Loaner, on_delete=models.CASCADE, blank=False, null=True)
    materials = models.ManyToManyField(LoanMaterial)

    def __str__(self):
        return "{0}".format(self.pk)



