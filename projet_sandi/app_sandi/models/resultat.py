from django.db import models
from ckeditor.fields import RichTextField
from app_sandi.models.prescription import Prescription

class Resultat(models.Model):
    id = models.BigAutoField(verbose_name="Code resultat", unique=True, primary_key = True, editable = False)
    examen=models.CharField(verbose_name="Examens", max_length=255)
    categorie=models.CharField(verbose_name="Catégorie", max_length=255)
    resultat_rapide=models.ForeignKey('self', models.SET_NULL, related_name="rapide_result", verbose_name="Résultat rapide", blank=True, null=True)
    result_prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, verbose_name="Prescription", blank=True, null=True)
    resultat_examen=RichTextField(blank=True, null=True)
    #valeur_reference = models.CharField(verbose_name="valeur de reférence", max_length=255,blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to='resultats', verbose_name="Fichier du résultat")
    date_mise_a_jour=models.DateField(verbose_name="date mise à jour", auto_now=True)
    date_creation=models.DateField(verbose_name="date de création", auto_now_add=True, editable=False)


    def __str__(self) -> str:
        if self.resultat_examen!="":
            return f" {self.resultat_examen}"
        elif self.resultat_rapide!="":
             return f" {self.resultat_rapide}"
        else:
             return None
             