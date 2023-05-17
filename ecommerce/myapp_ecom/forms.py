from django.forms import ModelForm

from django import forms
from . import models



class produitform(forms.ModelForm):

    class Meta:
        model = models.Produit
        fields = '__all__'

        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'prix': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)