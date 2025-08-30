from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import ClientSignupForm, LoginForm
from .models import SignUpClient

def signup_client(request):
    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte client créé avec succès ! Connectez-vous maintenant.")
            return redirect('LoginClient')
    else:
        form = ClientSignupForm()
    
    return render(request, 'SignUpClient.html', {'form': form})


def LoginClient(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                try:
                    client = SignUpClient.objects.get(user=user)
                    login(request, user) 

                    request.session['client_id'] = client.id
                    request.session['client_name'] = user.username

                    return redirect('afterLogin')
                except SignUpClient.DoesNotExist:
                    messages.error(request, "Ce compte n'est pas un compte client.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'LoginClient.html', {'form': form})


def afterLogin(request):
    return render(request, 'afterLogin.html')


def logout_view(request):
    logout(request)  
    return render(request,'logout.html')  
