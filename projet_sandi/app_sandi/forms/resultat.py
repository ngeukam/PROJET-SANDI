from django import forms
from app_sandi.models.resultat import Resultat
from ckeditor.fields import RichTextField
import ast

class ResultatForm(forms.ModelForm):

    error_css_class = 'error-field'
    required_css_class = 'required-field'
    examen = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "id":"examen"}), disabled=True, label=False, required=False)
    resultat_rapide = forms.ModelChoiceField(Resultat.objects.all().distinct('resultat_examen'), widget=forms.Select(attrs={"class":"form-control", "id" : "rapid"}), required=False)
    #resultat_examen = RichTextField(config_name = "default", blank=False)
    categorie = forms.CharField(widget=forms.HiddenInput(attrs={"class":"form-control"}), required=False)
    file = forms.FileField(widget=forms.FileInput(attrs={"id" : "attach",  "style" : "display: none"}), label=False, required=False)
   
    class Meta:
        model = Resultat
        
        fields = [
            "examen",
            "file",
            "resultat_rapide",
            "categorie",
            "resultat_examen",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)