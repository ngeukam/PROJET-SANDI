from django.db import models
from app_sandi.models.clinic import Clinic
from django.conf import settings
from .laboratoire import Laboratoire
from .patient import Patient

class Prescription(models.Model):
    id = models.BigAutoField(verbose_name="Code prescription", unique=True, primary_key = True, editable = False)
    examen=models.CharField(verbose_name="Examens", max_length=255)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    laboratoire = models.ForeignKey(Laboratoire, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Prescripteur", null=True)
    note = models.TextField(verbose_name="Note", blank=True, max_length=255, null=True)
    clinic = models.ForeignKey(Clinic,verbose_name="Clinic actuelle", on_delete=models.CASCADE, null=True)
    status=models.BooleanField(default=0)
    info=models.BooleanField(default=0)
    date_mise_a_jour=models.DateField(verbose_name="Date mise à jour", auto_now=True)
    date_creation=models.DateField(verbose_name="Date de création", auto_now_add=True, editable=False)
    date_prelevement=models.DateField(verbose_name="Date de prélèvement", blank=True, null=True)

    def __str__(self) -> str:
        return f"P{self.id} {self.examen}"