from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views  import generic
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm


def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None  and user.is_active:
                login(request, user)
                messages.success(
                        request, f"Vous êtes connecté(e) {username}")
                if user.is_doctor:
                        return redirect('creer-prescriptions')
                elif user.user_type == 3:
                        return redirect('creer-patients')
                elif user.user_type == 4:
                        return redirect('prescriptions')
                else:
                       return redirect('home')
        else:
            messages.error(request, "Veillez bien entrer les données du compte")
            
    else:
        form = AuthenticationForm()
    return render(request, "sandi/home.html", {"form": form})

class LogOutView(generic.RedirectView):
    url = reverse_lazy('home')
    success_message = " Vous êtes déconnecté(e)!"
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)

def Change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a étè modifié avec succés!')
            return redirect('home')
        else:
            pass
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'sandi/change_password.html', {
        'form': form
    })