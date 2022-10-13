from operator import *
from django import forms
from app_sandi.models.reference import Reference
from app_sandi import examens as examens_constants

class ReferenceForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    examen=forms.ChoiceField(widget=forms.Select(attrs={"id":"dynamic-option-creation"}),choices=examens_constants.EXAMEN_TYPE_CHOICES, required=True)
    valeur_reference=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "rows":"4"}), required=False)
    
    class Meta:
        model=Reference
        fields=[
            "examen","valeur_reference"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        