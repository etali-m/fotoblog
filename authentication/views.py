from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import login, authenticate, logout #les methodes pour l'authentification et le connexion
from django.views.generic import View #Nécessaire pour utiliser les vues basées sur les classes

#the class view for the login page
class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message':message})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form':form, 'message':message})

#la vue pour la deconnexion d'un utilisateur
def logout_user(request):
    logout(request)
    return redirect('login')
