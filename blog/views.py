from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blog.models import Photo

from . import forms
from . import models

# Create your views here.
@login_required
def home(request):
    photos = models.Photo.objects.all() #on recupère toutes les photos
    return render(request, 'blog/home.html', context={'photos':photos})

#vue pour l'ajout de nouvelle photo
@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user 
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form':form})