import datetime
import os
from django.views  import generic
from app_sandi.models.resultat import Resultat
from django.shortcuts import redirect, render
from app_sandi.models.prescription import Prescription
from app_sandi.models.clinic import Clinic
from app_sandi.models.login import User
from django.http import HttpResponse
from django.views.generic import View
from app_sandi.models.reference import Reference
from app_sandi.models.login import UserProfile
from projet_sandi.utils import render_to_pdf
from pathlib import Path

def list_resultat (request):
    user = request.user
    connected_user = UserProfile.objects.get(user=user)
    clinics = Clinic.objects.filter(compte_clinic=connected_user)
    prescriptions = Prescription.objects.filter(clinic__in=clinics)
    list_resultat=Resultat.objects.filter(result_prescription__in=prescriptions).order_by('-result_prescription_id').distinct('result_prescription_id')
    return render(request, 'sandi/patient/list_resultat.html', {'list_resultat':list_resultat})

class GeneratePdf(View):
    def get(self, request, id, *args, **kwargs):
        user = request.user
        user_connect=False
        resultats = Resultat.objects.filter(result_prescription=id).values('examen','categorie','resultat_examen','resultat_rapide','result_prescription')
        one_resultat = Resultat.objects.filter(result_prescription=id)[:1]
        rid=Resultat.objects.filter(resultat_rapide_id__isnull=False).filter(result_prescription=id).values('id')
        valeurs_resultats=Resultat.objects.filter(rapide_result__in=rid).values('resultat_examen','id')
        valeurs_reference =  Reference.objects.filter(examen__in=resultats.values_list('examen'))
        #Cet algo consistera à faire un filtre des catégories doubles des examens
        tab=[]
        while len(tab)<len(resultats):
            for i in range(len(resultats)):
                tab.append(resultats[i]['categorie'])
            tab
        tab_2=[]
        for x in tab:
            if tab.count(x)>1:
                tab_2.append(x)
        filter_tab_cat = [*set(tab_2)]
        BASE_DIR = Path(__file__).resolve().parent.parent
        path = os.path.join( BASE_DIR , 'static')
        pdf = render_to_pdf('sandi/patient/resultat.html', {'resultats': resultats, 'one_resultat':one_resultat, 'filter_tab_cat':filter_tab_cat, 'path':path, 'valeurs_reference':valeurs_reference, 'valeurs_resultats':valeurs_resultats})
        return HttpResponse(pdf, content_type='application/pdf')