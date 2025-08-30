from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import SignUpClient

class ClientSignupForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse e-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = SignUpClient
        fields = ['adresse', 'telephone']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Cet e-mail est déjà utilisé.")
        return email

    def save(self, commit=True):
     if User.objects.filter(username=self.cleaned_data['username']).exists():
        raise ValidationError("Ce nom d'utilisateur est déjà utilisé.")

     user = User.objects.create_user(
        username=self.cleaned_data['username'],
        email=self.cleaned_data['email'],
        password=self.cleaned_data['password']
     )

     client = super().save(commit=False)
     client.user = user  # ✅ ici le champ est 'user', PAS 'username'
     if commit:
        client.save()
     return client

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
