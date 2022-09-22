from django.contrib.auth import get_user_model #this allow to get the User Model without importing it directly
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'role')