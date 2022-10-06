from django.contrib.auth import get_user_model #this allow to get the User Model without importing it directly
from django.contrib.auth.forms import UserCreationForm

from django import forms

#formulaire pour l'inscription d'un utilisateur
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_photo',)


