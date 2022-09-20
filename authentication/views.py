from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import login, authenticate, logout #les methodes pour l'authentification et le connexion

# views.py
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})

#la vue pour la deconnexion d'un utilisateur
def logout_user(request):
    logout(request)
    return redirect('login')
