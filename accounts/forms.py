from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class Cadastro(forms.ModelForm):
    class Meta:
        model = User
        exclude = ()
        # fields = ('first_name', 'last_name', 'username', 'password')
