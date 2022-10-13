from app_sandi.models.patient import Patient
from django.shortcuts import render, redirect
from app_sandi.forms.patient import PatientForm
from django.views  import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from app_sandi.models.clinic import Clinic
from app_sandi.models.login import UserProfile
from django.conf import settings
from app_sandi.models.login import User
import uuid
from operator import concat

def list_patient(request):
    selected="patient"
       #on recupère l'utilisateur courant
    user = request.user
    connected_user = UserProfile.objects.get(user=user)
    """on recupére les cliniques dans lesquelles travaillent l'utilisateur connecté"""
    clinic_of_user=Clinic.objects.filter(compte_clinic=connected_user)
    list_patient = Patient.objects.filter(clinic_patient__in=clinic_of_user).order_by('-date_creation')
    return render(request, "sandi/patient/list_patient.html", {'list_patient':list_patient})


class CreatePatient(generic.CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "sandi/infirmier.html"

    def get(self, request):
           #on recupère l'utilisateur courant
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def functionuuidcode(self):
        id = uuid.uuid4()
        id = str(id)
        sliced_id = slice(3)
        sliced_id2 = slice(9,11)
        code = concat(id[sliced_id].upper(), id[sliced_id2].upper())
        return code
    
    def post(self, request):
        user = request.user
        connected_user = UserProfile.objects.get(user=user)
        clinic = Clinic.objects.get(compte_clinic=connected_user)#on va limiter la sortie à 1
        if request.method == "POST":
            form=PatientForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.nom = form.cleaned_data.get('nom')
                obj.prenom = form.cleaned_data.get('prenom')
                obj.telephone = form.cleaned_data.get('telephone')
                obj.code = self.functionuuidcode()
                obj.age = form.cleaned_data.get('age')
                obj.quartier = form.cleaned_data.get('quartier')
                obj.clinic_patient = clinic
                obj.save()
                messages.success(
                        request, f"Le patient {obj.nom} {obj.prenom} de code {obj.code}  a étè créé, il est temps de faire sa prescription.")
        return redirect('patients')

class UpdatePatient(SuccessMessageMixin, generic.UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "sandi/infirmier.html"
    success_message = " Patient modifié avec succès!"
    def get_success_url(self):
        return reverse_lazy("detail-patient", kwargs={"pk": self.object.id}) 