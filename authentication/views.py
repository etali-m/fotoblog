from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect


from . import forms

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #auto login the user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form':form})


#fonction pour l'ajour d'une photo de profile
def upload_profile_photo(request):
    form = forms.UploadProfilePhotoForm(instance=request.user) #on instancie le formulaire avec les informations sur l'utilisateur qui est connecté
    if request.method == 'POST':
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'authentication/upload_profile_photo.html', context={'form':form})
