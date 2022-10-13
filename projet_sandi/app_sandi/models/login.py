from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .clinic import Clinic
from .laboratoire import Laboratoire
from app_sandi import constants as user_constants
from django.utils import timezone
from app_sandi.managers import UserManager


class User(AbstractUser):
    username = models.CharField(max_length = 50, null = True, unique = True)
    email = models.EmailField(null=True,  blank = True, max_length = 50)
    is_active = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.PositiveSmallIntegerField(choices=user_constants.USER_TYPE_CHOICES)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    objects = UserManager()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="user_profile")
    user_lab=models.ManyToManyField(Laboratoire, related_name="compte_laboratoire", blank=True)
    user_clinic=models.ManyToManyField(Clinic, related_name="compte_clinic", blank=True)
    telephone_regex=RegexValidator(
        regex="[0-9]{9}", message="Veuillez entrer un numéro de télèphone valide"
    )
    telephone=models.CharField(validators=[telephone_regex],max_length=9, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    """is_doctor=models.BooleanField(default=False, verbose_name='Docteur')
    is_infirmier=models.BooleanField(default=False, verbose_name='Infimier(e)')
    is_technicien=models.BooleanField(default=False, verbose_name='Technicien')
    user_lab=models.ManyToManyField(Laboratoire, related_name="compte_laboratoire", blank=True)
    user_clinic=models.ManyToManyField(Clinic, related_name="compte_clinic", blank=True)
    telephone_regex=RegexValidator(
        regex="[0-9]{9}", message="Veuillez entrer un numéro de télèphone valide"
    )
    telephone=models.CharField(validators=[telephone_regex],max_length=9, blank=True)"""
   
    