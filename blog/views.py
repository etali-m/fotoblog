from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

from blog.models import Photo

from . import forms
from . import models

# Create your views here.
@login_required
def home(request):
    photos = models.Photo.objects.all() #on recupère toutes les photos
    blogs = models.Blog.objects.all() #On recupère tout post du blog
    return render(request, 'blog/home.html', context={'photos':photos, 'blogs':blogs})

#vue pour l'ajout de nouvelle photo
@login_required
@permission_required('blog.add_photo', raise_exception=True) #permet de s'assurer que l'utilisateur qui est connecté a les droits d'ajout de photos
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

@login_required
@permission_required('blog.add_photo','blog.add_blog')
def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Primary Author'})
            return redirect('home')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/create_blog_post.html', context)


@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog':blog})


@login_required
@permission_required('blog.change_blog')
def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST: #si le formulaire de modification fait partir de la requet POST
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        #Si le formulaire de supprésion est validé on supprime me poste        
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
        
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', context=context)


@login_required
def follow_users(request):
    form = forms.FollowUserForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html', context={'form':form})