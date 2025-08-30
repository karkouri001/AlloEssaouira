from django import forms
from django.contrib.auth.models import User
from .models import Livreur

class LivreurSignupForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = Livreur
        fields = ['telephone']

    def save(self, commit=True):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
         return None

        user = User.objects.create_user(
           username=self.cleaned_data['username'],
           email=self.cleaned_data['email'],
           password=self.cleaned_data['password']
        )

        livreur = super().save(commit=False)
        livreur.user = user
        if commit:
             livreur.save()
        return livreur



class LoginLivreurForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
