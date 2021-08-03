from .models import Album, Image
from django.contrib.auth.models import User
from django import forms


class EditForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['client']

