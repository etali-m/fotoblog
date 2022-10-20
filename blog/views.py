from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required 
from django.db.models import Q
from django.core.paginator import Paginator

from blog.models import Photo
from itertools import chain

from . import forms
from . import models

# Create your views here.
@login_required
def home(request): 
    #on va recupérer les posts des personnes qui sonst suivies par l'utilisateur qui 
    #est connecté
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) |
        Q(starred=True)
        )
    #On va recupérer les photos qui ont été uploader pour les utilisateurs qu'on suit
    photos = models.Photo.objects.filter(uploader__in=request.user.follows.all()).exclude(
        blog__in=blogs
    )

    blogs_and_photos = sorted(
        chain(blogs, photos), key=lambda instance: instance.date_created, reverse=True
    )
    ## la pagination pour la page d'accueil
    paginator = Paginator(blogs_and_photos, 6)
    page_number = request.GET.get('page') #on recupère le numero de la page dans les paramètres de l'url
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'blog/home.html', context=context)

#vue pour afficher unique les photos des personnes qu'on follow
@login_required
def photo_feed(request):
    photos = models.Photo.objects.filter(uploader__in=request.user.follows.all())
    ##pagination pour les photos
    paginator = Paginator(photos, 6)
    page_number = request.GET.get('page')
    photo_obj = paginator.get_page(page_number)
    context = {
        'photo_obj':photo_obj,
    }
    return render(request, 'blog/photo_feed.html', context=context)


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
            blog.contributors.add(request.user, through_defaults={'contributions': 'Primary Author'})
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