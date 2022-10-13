from app_sandi.models.prescription import Prescription
from app_sandi.models.patient import Patient
from django.shortcuts import render, redirect
from app_sandi.forms.prescription import PrescriptionForm
from django.views  import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from app_sandi.models.laboratoire import Laboratoire
from django.contrib import messages
from app_sandi.models.clinic import Clinic
from app_sandi.forms.resultat import ResultatForm
from app_sandi.models.resultat import Resultat
import ast
from django.forms import modelformset_factory
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from app_sandi.models.login import UserProfile
from app_sandi import examens as examens_constants
from django.http.response import HttpResponseRedirect, HttpResponse


def list_prescription(request):
    selected="prescription"
    """On fait un filtre qui permet de faire que chaque laboratoire voit uniquement la liste des prescriptions
    qui lui a étè affectée"""
    #on recupère l'utilisateur courant
    user = request.user
    connected_user = UserProfile.objects.get(user=user)
    """on veriéfie que l'utilisateur connecté travaille dans une clinique, elle servira à
    afficher uniquement les prescriptions des cliniques dans lesquelles l'utilisteur exerce"""
    clinics = Clinic.objects.filter(compte_clinic=connected_user).all()
    #On recupère la liste de laboratoire dans lequel l'utilisateur courant exerce
    laboratoires = Laboratoire.objects.filter(compte_laboratoire=connected_user).all()
    #On fait une sous requête avec les reponses des requêtes plus haute
    list_prescription=Prescription.objects.filter(laboratoire__in=laboratoires, ) | Prescription.objects.filter(clinic__in=clinics).order_by('-id')
    return render(request, "sandi/patient/list_prescription.html", {'list_prescription':list_prescription, 'clinics':clinics, 'laboratoires':laboratoires})

class CreatePrescription(generic.CreateView):
    model=Prescription
    form_class = PrescriptionForm
    template_name = "sandi/docteur.html"

    def get(self, request):
        patients=Patient.objects.all()
        laboratoires=Laboratoire.objects.all()
        clinics = Clinic.objects.all()
        form = self.form_class
        return render(request, self.template_name, {'form': form, 'patients': patients,'laboratoires': laboratoires, 'clinics' : clinics})
    
    def post(self, request):
        user = request.user
        connected_user = UserProfile.objects.get(user=user)
        clinics = Clinic.objects.filter(compte_clinic=connected_user)
        if request.method == "POST":
            form=PrescriptionForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.examen = form.cleaned_data.get('examen')
                obj.note = form.cleaned_data.get('note')
                obj.info = form.cleaned_data.get('info')
                obj.patient = form.cleaned_data.get('patient')
                obj.laboratoire = form.cleaned_data.get('laboratoire')
                obj.clinic = form.cleaned_data.get('clinic')
                obj.date_prelevement = form.cleaned_data.get('date_prelevement')
                obj.user = request.user
                for clinic in clinics:
                    if clinic == obj.clinic:
                        obj.save()
                        messages.success(
                        request, f"Les examens prescrits au patient {obj.patient} ont étè envoyés au laboratoire {obj.laboratoire}.")
                        clinic_actuelle = Clinic.objects.get(patient=obj.patient_id)
                        if clinic_actuelle!=obj.clinic:
                            patient_update = Patient.objects.filter(pk=obj.patient_id).update(clinic_patient_id=obj.clinic_id)
                        break
                    else:
                        messages.error(
                        request, f"Désolè vous ne travaillez pas dans la clinique {obj.clinic}.")
        return redirect('creer-prescriptions')

class UpdatePrescription(SuccessMessageMixin, generic.UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = "sandi/docteur.html"

    """def form_view(request):
        all_exam = examens_constants.EXAMENS_DICT_CHOICES
        return render(request, 'sandi/docteur.html', all_exam)"""

    def post(self, request, pk):
        user = request.user
        connected_user = UserProfile.objects.get(user=user)
        clinics = Clinic.objects.filter(compte_clinic=connected_user)
        if request.method == "POST":
            form=PrescriptionForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.examen = form.cleaned_data.get('examen')
                obj.note = form.cleaned_data.get('note')
                obj.info = form.cleaned_data.get('info')
                obj.patient = form.cleaned_data.get('patient')
                obj.laboratoire = form.cleaned_data.get('laboratoire')
                obj.clinic = form.cleaned_data.get('clinic')
                obj.date_prelevement = form.cleaned_data.get('date_prelevement')
                obj.user = user
                for clinic in clinics:
                    if clinic == obj.clinic:
                        prescription_update = Prescription.objects.filter(id=pk).update(
                            examen=obj.examen,
                            note=obj.note,
                            info=obj.info,
                            patient=obj.patient,
                            laboratoire=obj.laboratoire,
                            clinic=obj.clinic,
                            user= obj.user
                            )
                        messages.success(
                        request, f"Prescription du patient {obj.patient} modifiée avec succès!")
                        break
                    else:
                        messages.error(
                        request, f"Désolè vous ne travaillez pas dans la clinique {obj.clinic}.")
                        #return reverse_lazy("mise-a-jour-prescriptions", kwargs={"pk":pk})
        #return redirect('prescriptions')
            #return HttpResponse('Form not valid')
            return HttpResponseRedirect(reverse_lazy("detail-prescription", kwargs={"prescription_id": pk}))

    #success_message = f"Prescription du patient {Patient.nom} modifiée avec succès!"
    """def get_success_url(self):
        return reverse_lazy("detail-prescription", kwargs={"prescription_id": self.object.id})"""

@method_decorator(csrf_exempt, name='dispatch')
def post_resultat_view (request, prescription_id):
            prescription = Prescription.objects.get(id = prescription_id)
            form = ResultatForm()
            resultats = Resultat.objects.filter(result_prescription = prescription_id)[:1]
            #obj = get_object_or_404(Resultat, id = id, user = request.user)
            template_name = "sandi/patient/detail_prescription.html"
            #qs = On recupére tous les résultats de la prescription en cours
            actual_prescription=Prescription.objects.filter(id = prescription_id)
            all_list_exam = actual_prescription.values('examen')
            tab_list = list(all_list_exam)
            filter_tab_list = tab_list[0]['examen']
            #grâce à la fonction ast, on fait une conversion du string en array
            array_tab = ast.literal_eval(filter_tab_list)
            nbr_res = len(array_tab)
            #cette petite fonction nous permet de récupèrer les exames prescrits afin d'initialiser le formset
            def GetExamen() :
                D = examens_constants.EXAMENS_DICT_CHOICES
                Elt = array_tab
                Tabkeys = list(D.keys())
                Exam_list = []
                Cat_list = []
                while len(Cat_list)<len(Tabkeys):
                    for i in range(0, len(Tabkeys)):
                        for s in Elt:
                            if s in D[Tabkeys[i]]:
                                Cat_list.insert(0, Tabkeys[i])
                                Exam_list.insert(0, s)
                Exam_list
                Cat_list
                            
                initialtab=[]
                while len(initialtab)<len(Exam_list):
                            for examen, categorie in zip(Exam_list, Cat_list):
                                    initialtab.insert(0, {'examen':examen, 'categorie':categorie})
                            initialtab
                    
                return initialtab
            
            ResultatFormSet = modelformset_factory(Resultat, form = ResultatForm, extra=nbr_res, validate_max=True )
            formset = ResultatFormSet(queryset=Resultat.objects.none(),initial = GetExamen())
            context = {
                "formset" : formset,
                "prescription" : prescription,
                "resultats":resultats,
            }
            
            if request.method == "POST":
                formset = ResultatFormSet(request.POST or None, request.FILES, queryset=Resultat.objects.none(),initial = GetExamen())
                if formset.is_valid():
                    instances = formset.save(commit=False)
                    for instance in instances :
                        instance.result_prescription = prescription
                        if instance.resultat_rapide or instance.resultat_file or instance.resultat_examen:
                            instance.save()
                            prescription_update = Prescription.objects.filter(pk=prescription_id).update(status=1)
                            messages.success(
                        request, f"Les résultats de la prescription P{prescription_id} ont étè bien envoyés au centre de santé {prescription.clinic}.")
                else:
                    messages.error(
                        request, f"Envoi échoué, joindre un fichier ou remplir les champs.")
                return redirect ('prescriptions')
            return render (request, template_name, context)