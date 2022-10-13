from operator import *
from re import M
from django.core.validators import RegexValidator
from django.db import models
from app_sandi.models.clinic import Clinic

import uuid

class Patient(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    nom=models.CharField(max_length=255)
    prenom=models.CharField(max_length=255)
    telephone_regex=RegexValidator(
        regex="[0-9]{9}", message="Veuillez entrer un numéro de télèphone valide"
    )
    telephone=models.CharField(validators=[telephone_regex],max_length=9, blank=True, null=True)
    code=models.CharField(max_length=5, unique=True)
    sexe=models.CharField(max_length=1, blank=True)
    age=models.CharField(max_length=3, blank=True, null=True)
    quartier=models.CharField(max_length=255, blank=True, null=True)
    clinic_patient = models.ForeignKey(Clinic, verbose_name="Clinique du patient",on_delete=models.CASCADE, null=True, blank=False)
    date_mise_a_jour=models.DateField(verbose_name="date mise à jour", auto_now=True)
    date_creation=models.DateField(verbose_name="date de création", auto_now_add=True, editable=False)

    def __str__(self) -> str:
        if self.sexe == 'M':
            genre = 'M'
        else:
            genre = 'Mme'
        return f"{genre} {self.nom} {self.prenom} {self.code}"
