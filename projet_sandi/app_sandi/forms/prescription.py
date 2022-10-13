from operator import *
from django import forms
from app_sandi.models.prescription import Prescription
from app_sandi.models.patient import Patient
from app_sandi.models.laboratoire import Laboratoire
from app_sandi.models.clinic import Clinic
from app_sandi import examens as examens_constants



class PrescriptionForm(forms.ModelForm):
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    date_prelevement=forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class":"form-control", "id":"mdate", "placeholder":"Date"}), required=False)
    examen=forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={"id":"multi-value-select"}),choices=examens_constants.EXAMEN_TYPE_CHOICES, required=True)
    note=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "rows":"4"}), required=False)
    info=forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-check-input"}), required=False)
    patient=forms.ModelChoiceField(Patient.objects.all(), widget=forms.Select(attrs={"class":"form-control",  "id":"dynamic-option-creation"}))
    laboratoire=forms.ModelChoiceField(Laboratoire.objects.all(), widget=forms.Select(attrs={"class":"form-control",  "id":"automatic-selection"}))
    clinic=forms.ModelChoiceField(Clinic.objects.all(), widget=forms.Select(attrs={"class":"form-control",  "id":"single-select"}))

    
    class Meta:
        model=Prescription
        fields=[
            "examen","patient", "laboratoire", "note", "info", "clinic", "date_prelevement"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        