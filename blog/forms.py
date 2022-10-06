from re import U
from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

#formulaire pour l'ajout de photo
class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']

#formulaire pour l'ajout d'un nouveau post dans le blog
class BlogForm(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ['title', 'content']
        

class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Blog
        fields = ['title', 'content']


class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True)

#Cette classe permet à un subscriber de suivre un createur
class FollowUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['follows']