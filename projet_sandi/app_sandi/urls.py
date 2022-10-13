from django.urls import path
from django.views.generic import DetailView
from .models.patient import Patient
from .models.reference import Reference
from .views import patients, login, prescription, resultat, reference
from django.conf.urls.static import static
from django.conf import settings
from .views.resultat import GeneratePdf
from django.contrib.auth import views as auth_views


urlpatterns = [
    #login
    path('', login.Login, name="home"),
    path('deconnexion', login.LogOutView.as_view(), name='deconnexion'),
    path('password', login.Change_password, name='change-password'),
    #Patients
    path('patients', patients.list_patient, name="patients"),
    path('patients/creer-patient', patients.CreatePatient.as_view(), name="creer-patients"),
    path('patients/mise-a-jour/<str:pk>', patients.UpdatePatient.as_view(), name="mise-a-jour-patients"),
    path('patients/<str:pk>', DetailView.as_view(model=Patient, template_name="sandi/patient/detail_patient.html"), name="detail-patient"),

    #Prescriptions des examens
    path('prescriptions', prescription.list_prescription, name="prescriptions"),
    path('prescriptions/creer-prescription', prescription.CreatePrescription.as_view(), name="creer-prescriptions"),
    path('prescriptions/mise-a-jour/<int:pk>', prescription.UpdatePrescription.as_view(), name="mise-a-jour-prescriptions"),
    path('prescriptions/<int:prescription_id>', prescription.post_resultat_view, name="detail-prescription"),

    #Resultats des prescriptions
    path('resultats', resultat.list_resultat, name="resultats"),
    path('resultat-pdf/<int:id>', GeneratePdf.as_view(), name="resultat-pdf"),

    #Params des resultats
    path('valeurs-de-reference', reference.list_reference, name="valeurs-reference"),
    path('ajout-valeur-reference', reference.CreateReference.as_view(), name="creer-valeur-reference"),
    path('valeur-de-reference/<int:pk>', DetailView.as_view(model=Reference, template_name="sandi/detail_valeur_reference.html"), name="detail-valeur-reference"),
    path('valeur-de-reference/mise-a-jour/<int:pk>', reference.UpdateReference.as_view(), name="mise-a-jour-valeur-reference"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)