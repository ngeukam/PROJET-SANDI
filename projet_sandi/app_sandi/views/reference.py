from app_sandi.models.reference import Reference
from django.shortcuts import render, redirect
from app_sandi.forms.reference import ReferenceForm
from django.views  import generic
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

def list_reference(request):
    selected="reference"
    list_reference = Reference.objects.all()
    return render(request, "sandi/list_valeur_reference.html", {'list_reference':list_reference})

class CreateReference(generic.CreateView):
    model = Reference
    form_class = ReferenceForm
    template_name = "sandi/valeur_reference.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        if request.method == "POST":
            form=ReferenceForm(request.POST or None)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.examen = form.cleaned_data.get('examen')
                obj.valeur_reference = form.cleaned_data.get('valeur_reference')
                obj.save()
                messages.success(
                        request, f"La valeur de refèrence a étè bien enregistrée.")
        return redirect('valeurs-reference')

class UpdateReference(SuccessMessageMixin, generic.UpdateView):
    model = Reference
    form_class = ReferenceForm
    template_name = "sandi/valeur_reference.html"
    success_message = " Valeur de refèrence modifiée avec succès!"
    def get_success_url(self):
        return reverse_lazy("detail-valeur-reference", kwargs={"pk": self.object.id}) 