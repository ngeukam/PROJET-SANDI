from django import forms
from app_sandi.models.patient import Patient
from app_sandi.models.clinic import Clinic
from django.contrib.auth import get_user_model

User=get_user_model()

class PatientForm(forms.ModelForm):
    def ClinicPatient(request):
        user = request.user
        connected_user = User.objects.get(username=user)
        return connected_user
    SEXE_CHOICES = [('M','M'), ('F','F')]
    error_css_class = 'error-field'
    required_css_class = 'required-field'
    sexe=forms.CharField(widget=forms.Select(attrs={"class":"form-control"}, choices=SEXE_CHOICES))
    nom=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Entrer le nom du patient"}))
    prenom=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Entrer le prénom du patient"}))
    telephone=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Entrer le télèphone du patient"}), required=False)
    age=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Entrer l'âge du patient"}))
    quartier=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Entrer le quartier du patient"}), required=False)
    #code=forms.CharField(widget=forms.TextInput(attrs={"readonly":True, "class":"form-control","placeholder":"Cliquer sur Code", "id":"code_patient"}))


    class Meta:
        model=Patient
        fields=("nom", "prenom", "telephone", "quartier", "age", "sexe")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
