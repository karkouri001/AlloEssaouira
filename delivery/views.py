from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import LivreurSignupForm, LoginLivreurForm
from .models import Livreur, Livraison
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Commande


def login_livreur(request):
    if request.method == 'POST':
        form = LoginLivreurForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if Livreur.objects.filter(user=user).exists():
                    login(request, user)
                    livreur = Livreur.objects.get(user=user)
                    request.session['livreur_name'] = livreur.user.username
                    request.session['livreur_id'] = livreur.id
                    return redirect('commandes_disponibles')
                else:
                    messages.error(request, "Ce n'est pas un compte livreur.")
            else:
                messages.error(request, "Identifiants incorrects.")
    else:
        form = LoginLivreurForm()
    return render(request, 'LoginLivreur.html', {'form': form})

@login_required
def after_login_livreur(request):
    try:
        livreur = Livreur.objects.get(user=request.user)
        livraisons = Livraison.objects.filter(livreur=livreur).order_by('-date_livraison')
    except Livreur.DoesNotExist:
        livraisons = []

    return render(request, 'AfterLoginLivreur.html', {
        'livraisons': livraisons
    })


@login_required
def commandes_disponibles(request):
    commandes_non_attribuees = Commande.objects.filter(
        livraison__isnull=True
    ).order_by('-date_commande')

    return render(request, 'commandes_disponibles.html', {
        'commandes': commandes_non_attribuees
    })

@login_required

def accepter_commande(request, commande_id):
    if request.method == 'POST':
        livreur = Livreur.objects.get(user=request.user)
        commande = get_object_or_404(Commande, id=commande_id)

        if not hasattr(commande, 'livraison'):
            Livraison.objects.create(
                commande=commande,
                livreur=livreur,
                statut='en_cours'
            )
            commande.statut = 'en_cours'  
            commande.save()
        return redirect('commandes_disponibles')
    return redirect('commandes_disponibles')


@login_required
def terminer_livraison(request, livraison_id):
    livraison = get_object_or_404(Livraison, id=livraison_id, livreur__user=request.user)
    livraison.statut = 'terminee'
    livraison.save()

    commande = livraison.commande
    commande.statut = 'livree' 
    commande.save()

    return redirect('after_login_livreur')

def logout_livreur(request):
    logout(request)
    return redirect('logout')
