from django.core.validators import RegexValidator
from django.db import models
import uuid

class Clinic(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    nom=models.CharField(max_length=255)
    quartier=models.CharField(max_length=255)
    ville=models.CharField(max_length=255)
    telcli_regex=RegexValidator(
        regex="[0-9]{9}", message="Veuillez entrer un numéro de télèphone valide"
    )
    telcli=models.CharField(validators=[telcli_regex],max_length=9, blank=True, verbose_name='Télèphone clinique')
    telpro_regex=RegexValidator(
        regex="[0-9]{9}", message="Veuillez entrer un numéro de télèphone valide"
    )
    telpro=models.CharField(validators=[telpro_regex],max_length=9, blank=True, verbose_name='Télèphone propriétaire')
    lat=models.CharField(max_length=50, blank=True)
    long=models.CharField(max_length=50, blank=True)
    bp=models.CharField(max_length=10, blank=True)
    etat=models.BooleanField(default=False)
    date_mise_a_jour=models.DateField(verbose_name="date mise à jour", auto_now=True)
    date_creation=models.DateField(verbose_name="date de création", auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.nom} {self.ville} {self.quartier}"
