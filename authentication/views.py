from django.shortcuts import render, redirect

from . import forms
from django.contrib.auth import login, authenticate, logout #les methodes pour l'authentification et le connexion
from django.views.generic import View #Nécessaire pour utiliser les vues basées sur les classes

 
#la vue pour la deconnexion d'un utilisateur
def logout_user(request):
    logout(request)
    return redirect('login')
