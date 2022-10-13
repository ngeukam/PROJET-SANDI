from django.db import models


class Reference(models.Model):
    id = models.BigAutoField(unique=True, primary_key = True, editable = False)
    examen=models.CharField(unique=True, verbose_name="Examen", max_length=255)
    valeur_reference = models.TextField(verbose_name="valeur de reférence", max_length=255,blank=True, null=True)
    date_creation=models.DateField(verbose_name="Date de création", auto_now_add=True, editable=False)

    def __str__(self) -> str:
        return f" {self.examen} {self.valeur_reference}"
      
             